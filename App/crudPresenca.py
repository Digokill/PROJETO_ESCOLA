from flask import Flask, request, jsonify
from flasgger import Swagger
import Util.bd as bd
import base64

from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter

from app import app, db
from models import  Presenca

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

@app.route('/presencas', methods=['POST'])
def add_presenca():
    """
    Registrar uma nova presença
    ---
    tags:
      - Presenças
    parameters:
      - in: body
        name: body
        required: true
        description: Dados da presença a ser registrada
        schema:
          type: object
          properties:
            aluno_id:
              type: integer
              example: 1
            data:
              type: string
              format: date
              example: "2023-10-01"
            presente:
              type: boolean
              example: true
    responses:
      201:
        description: Presença registrada com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Presença registrada com sucesso!"
      400:
        description: Erro na requisição
    """
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    cursor = conn.cursor()
    data = request.get_json()
    try:
        nova_presenca = Presenca(
            aluno_id=data['aluno_id'],
            data=data['data'],
            presente=data['presente']
        )
        db.session.add(nova_presenca)
        db.session.commit()
        return jsonify({'message': 'Presença registrada com sucesso!'}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
