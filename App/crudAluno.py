from flask import Flask, request, jsonify
from flasgger import Swagger
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter
import Util.bd as bd
import base64

from flask import request, jsonify
from app import app, db
from models import Aluno

app = Flask(__name__)

# Configuração do Swagger
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

@app.route('/alunos', methods=['POST'])
def add_aluno():
    """
    Adicionar um novo aluno
    ---
    tags:
      - Alunos
    parameters:
      - in: body
        name: body
        required: true
        description: Dados do aluno a ser adicionado
        schema:
          type: object
          properties:
            nome_completo:
              type: string
              example: "João Silva"
            data_nascimento:
              type: string
              format: date
              example: "2010-05-15"
            turma_id:
              type: integer
              example: 1
    responses:
      201:
        description: Aluno adicionado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Aluno adicionado com sucesso!"
      400:
        description: Erro na requisição
    """
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    cursor = conn.cursor()
    data = request.get_json()
    try:
        novo_aluno = Aluno(
            nome_completo=data['nome_completo'],
            data_nascimento=data['data_nascimento'],
            turma_id=data['turma_id']
        )
        db.session.add(novo_aluno)
        db.session.commit()
        return jsonify({'message': 'Aluno adicionado com sucesso!'}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
