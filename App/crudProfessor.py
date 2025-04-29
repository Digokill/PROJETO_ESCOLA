from flask import Flask, request, jsonify
import Util.bd as bd
import base64

from app import app, db
from models import Professor
from flasgger import Swagger
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter

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

@app.route('/professores', methods=['POST'])
def add_professor():
    """
    Adicionar um novo professor
    ---
    tags:
      - Professores
    parameters:
      - in: body
        name: body
        required: true
        description: Dados do professor a ser adicionado
        schema:
          type: object
          properties:
            nome_completo:
              type: string
              example: "Maria Silva"
            especialidade:
              type: string
              example: "Matemática"
            turma_id:
              type: integer
              example: 1
    responses:
      201:
        description: Professor adicionado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Professor adicionado com sucesso!"
      400:
        description: Erro na requisição
    """
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    cursor = conn.cursor()
    data = request.get_json()
    try:
        novo_professor = Professor(
            nome_completo=data['nome_completo'],
            especialidade=data['especialidade'],
            turma_id=data['turma_id']
        )
        db.session.add(novo_professor)
        db.session.commit()
        return jsonify({'message': 'Professor adicionado com sucesso!'}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
