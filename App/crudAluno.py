from flask import Flask, request, jsonify
try:
    from flasgger import Swagger
except ImportError as e:
    raise ImportError("O módulo 'flasgger' não está instalado. Instale-o com 'pip install flasgger'.") from e
try:
    from prometheus_flask_exporter import PrometheusMetrics
except ImportError as e:
    raise ImportError("O módulo 'prometheus_flask_exporter' não está instalado. Instale-o com 'pip install prometheus-flask-exporter'.") from e
from prometheus_client import Counter
import Util.bd as bd
import base64

from flask import request, jsonify
from app import app, db
from models import Aluno
from logging_config import get_logger

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

logger = get_logger(__name__)

logger.info("CRUD Aluno iniciado com sucesso.")

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
    logger.info("Iniciando adição de um novo aluno.")
    conn = bd.create_connection()
    if conn is None:
        logger.error("Falha ao conectar ao banco de dados.")
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
        logger.info("Aluno adicionado com sucesso.")
        return jsonify({'message': 'Aluno adicionado com sucesso!'}), 201
    except Exception as e:
        logger.error(f"Erro ao adicionar aluno: {e}")
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos', methods=['POST'])
def criar_aluno():
    """
    Endpoint para criar um novo aluno.
    """
    return add_aluno()

@app.route('/alunos/<int:id>', methods=['GET'])
def ler_aluno(id):
    """
    Endpoint para ler informações de um aluno pelo ID.
    """
    logger.info(f"Lendo informações do aluno com ID {id}.")
    aluno = Aluno.query.get(id)
    if aluno:
        return jsonify({
            "id": aluno.id,
            "nome_completo": aluno.nome_completo,
            "data_nascimento": aluno.data_nascimento,
            "turma_id": aluno.turma_id
        }), 200
    else:
        logger.error(f"Aluno com ID {id} não encontrado.")
        return jsonify({"error": "Aluno não encontrado"}), 404

@app.route('/alunos/<int:id>', methods=['PUT'])
def atualizar_aluno(id):
    """
    Endpoint para atualizar informações de um aluno pelo ID.
    """
    logger.info(f"Atualizando informações do aluno com ID {id}.")
    data = request.get_json()
    aluno = Aluno.query.get(id)
    if aluno:
        try:
            aluno.nome_completo = data.get('nome_completo', aluno.nome_completo)
            aluno.data_nascimento = data.get('data_nascimento', aluno.data_nascimento)
            aluno.turma_id = data.get('turma_id', aluno.turma_id)
            db.session.commit()
            logger.info(f"Aluno com ID {id} atualizado com sucesso.")
            return jsonify({"message": "Aluno atualizado com sucesso!"}), 200
        except Exception as e:
            logger.error(f"Erro ao atualizar aluno: {e}")
            return jsonify({"error": str(e)}), 400
    else:
        logger.error(f"Aluno com ID {id} não encontrado.")
        return jsonify({"error": "Aluno não encontrado"}), 404

@app.route('/alunos/<int:id>', methods=['DELETE'])
def deletar_aluno(id):
    """
    Endpoint para deletar um aluno pelo ID.
    """
    logger.info(f"Deletando aluno com ID {id}.")
    aluno = Aluno.query.get(id)
    if aluno:
        try:
            db.session.delete(aluno)
            db.session.commit()
            logger.info(f"Aluno com ID {id} deletado com sucesso.")
            return jsonify({"message": "Aluno deletado com sucesso!"}), 200
        except Exception as e:
            logger.error(f"Erro ao deletar aluno: {e}")
            return jsonify({"error": str(e)}), 400
    else:
        logger.error(f"Aluno com ID {id} não encontrado.")
        return jsonify({"error": "Aluno não encontrado"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
