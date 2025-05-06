from flask import Flask, request, jsonify
import Util.bd as bd
import base64

from app import app, db
from models import Aluno, Turma, Pagamento, Presenca, Atividade, AtividadeAluno
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

@app.route('/atividades_alunos', methods=['POST'])
def add_atividade_aluno():
    """
    Registrar uma atividade para um aluno
    ---
    tags:
      - Atividades Alunos
    parameters:
      - in: body
        name: body
        required: true
        description: Dados da atividade do aluno a ser registrada
        schema:
          type: object
          properties:
            aluno_id:
              type: integer
              example: 1
            atividade_id:
              type: integer
              example: 2
            nota:
              type: number
              format: float
              example: 9.5
    responses:
      201:
        description: Atividade do aluno registrada com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Atividade do aluno registrada com sucesso!"
      400:
        description: Erro na requisição
    """
    logger.info("Iniciando registro de uma atividade para um aluno.")
    conn = bd.create_connection()
    if conn is None:
        logger.error("Falha ao conectar ao banco de dados.")
        return jsonify({"error": "Failed to connect to the database"}), 500

    cursor = conn.cursor()
    data = request.get_json()
    try:
        nova_atividade_aluno = AtividadeAluno(
            aluno_id=data['aluno_id'],
            atividade_id=data['atividade_id'],
            nota=data['nota']
        )
        db.session.add(nova_atividade_aluno)
        db.session.commit()
        logger.info("Atividade do aluno registrada com sucesso.")
        return jsonify({'message': 'Atividade do aluno registrada com sucesso!'}), 201
    except Exception as e:
        logger.error(f"Erro ao registrar atividade do aluno: {e}")
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
