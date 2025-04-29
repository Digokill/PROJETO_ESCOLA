from flask import Flask, request, jsonify
import Util.bd as bd
import base64

from app import app, db
from models import Usuario
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter

app = Flask(__name__)

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

@app.route('/usuarios', methods=['POST'])
def add_usuario():
    """
    Adicionar um novo usuário
    ---
    tags:
      - Usuários
    parameters:
      - in: body
        name: body
        required: true
        description: Dados do usuário a ser adicionado
        schema:
          type: object
          properties:
            nome_usuario:
              type: string
              example: "admin"
            senha:
              type: string
              example: "123456"
            tipo_usuario:
              type: string
              example: "administrador"
    responses:
      201:
        description: Usuário adicionado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Usuário adicionado com sucesso!"
      400:
        description: Erro na requisição
    """
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    cursor = conn.cursor()
    data = request.get_json()
    try:
        novo_usuario = Usuario(
            nome_usuario=data['nome_usuario'],
            senha=data['senha'],
            tipo_usuario=data['tipo_usuario']
        )
        db.session.add(novo_usuario)
        db.session.commit()
        return jsonify({'message': 'Usuário adicionado com sucesso!'}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
