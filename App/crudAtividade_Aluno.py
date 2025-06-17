from flask import Flask, request, jsonify
from flask import Blueprint
import psycopg2
from flasgger import Swagger
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter
from logging_config import get_logger

logger = get_logger(__name__)

app = Flask(__name__)
swagger = Swagger(app)

# Configuração do Prometheus
metrics = PrometheusMetrics(app, default_labels={'app_name': 'flask_app'})

# Métricas personalizadas para sucessos e erros
success_counter = Counter(
    'http_success_count', 'Contagem de respostas HTTP com sucesso',
    ['endpoint', 'method', 'status']
)

error_counter = Counter(
    'http_error_count', 'Contagem de respostas HTTP com erro',
    ['endpoint', 'method', 'status']
)

@app.after_request
def after_request(response):
    """
    Middleware para capturar os retornos de todos os endpoints.
    """
    endpoint = request.path
    method = request.method
    status = response.status_code

    if 200 <= status < 300:
        success_counter.labels(endpoint=endpoint, method=method, status=str(status)).inc()
    else:
        error_counter.labels(endpoint=endpoint, method=method, status=str(status)).inc()

    return response

# Definir o Blueprint
atividades_alunos_bp = Blueprint('atividades_alunos', __name__)

logger.info("CRUD AtividadeAluno iniciado com sucesso.")

def get_db_connection():
    """
    Retorna uma conexão com o banco de dados PostgreSQL.
    """
    return psycopg2.connect(
        dbname="escola",
        user="faat",
        password="faat",
        host="db",
        port=5432
    )

@atividades_alunos_bp.route('/atividades_alunos', methods=['POST'])
def add_atividade_aluno():
    """
    Registrar uma atividade para um aluno.
    """
    logger.info("Iniciando registro de uma atividade para um aluno.")
    conn = get_db_connection()
    cur = conn.cursor()
    data = request.get_json()
    try:
        cur.execute(
            "INSERT INTO atividades_alunos (aluno_id, atividade_id, nota) VALUES (%s, %s, %s)",
            (data['aluno_id'], data['atividade_id'], data['nota'])
        )
        conn.commit()
        logger.info("Atividade do aluno registrada com sucesso.")
        return jsonify({'message': 'Atividade do aluno registrada com sucesso!'}), 201
    except Exception as e:
        logger.error(f"Erro ao registrar atividade do aluno: {e}")
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

# Registrar o Blueprint
app.register_blueprint(atividades_alunos_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
