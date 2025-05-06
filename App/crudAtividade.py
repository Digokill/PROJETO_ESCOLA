from flask import Flask, request, jsonify
import Util.bd as bd
import base64

from app import app, db
from models import  Atividade
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

@app.route('/atividades', methods=['POST'])
def add_atividade():
    """
    Cadastrar uma nova atividade
    ---
    tags:
      - Atividades
    parameters:
      - in: body
        name: body
        required: true
        description: Dados da atividade a ser cadastrada
        schema:
          type: object
          properties:
            descricao:
              type: string
              example: "Prova de Matemática"
            data_realizacao:
              type: string
              format: date
              example: "2023-10-15"
            turma_id:
              type: integer
              example: 1
    responses:
      201:
        description: Atividade cadastrada com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Atividade cadastrada com sucesso!"
      400:
        description: Erro na requisição
    """
    logger.info("Iniciando cadastro de uma nova atividade.")
    conn = bd.create_connection()
    if conn is None:
        logger.error("Falha ao conectar ao banco de dados.")
        return jsonify({"error": "Failed to connect to the database"}), 500

    cursor = conn.cursor()
    data = request.get_json()
    try:
        nova_atividade = Atividade(
            descricao=data['descricao'],
            data_realizacao=data['data_realizacao'],
            turma_id=data['turma_id']
        )
        db.session.add(nova_atividade)
        db.session.commit()
        logger.info("Atividade cadastrada com sucesso.")
        return jsonify({'message': 'Atividade cadastrada com sucesso!'}), 201
    except Exception as e:
        logger.error(f"Erro ao cadastrar atividade: {e}")
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
