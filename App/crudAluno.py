from flask import Blueprint, request, jsonify
from models import Aluno
from logging_config import get_logger

# from app import app, db
from models import Aluno
from logging_config import get_logger

# Configuração do Swagger
# swagger = Swagger(app)

# Definir o Blueprint
alunos_bp = Blueprint('alunos', __name__)

# # Configuração do Prometheus
# metrics = PrometheusMetrics(app, default_labels={'app_name': 'flask_app'})

# Métricas personalizadas para sucessos e erros
# success_counter = Counter(
#     'http_success_count', 'Contagem de respostas HTTP com sucesso',
#     ['endpoint', 'method', 'status']
# )

# error_counter = Counter(
#     'http_error_count', 'Contagem de respostas HTTP com erro',
#     ['endpoint', 'method', 'status']
# )

logger = get_logger(__name__)

logger.info("CRUD Aluno iniciado com sucesso.")

# @app.after_request
# def after_request(response):
#     """
#     Middleware para capturar os retornos de todos os endpoints.
#     """
#     endpoint = request.path
#     method = request.method
#     status = response.status_code

#     if 200 <= status < 300:
#         success_counter.labels(endpoint=endpoint, method=method, status=str(status)).inc()
#     else:
#         error_counter.labels(endpoint=endpoint, method=method, status=str(status)).inc()

#     return response

# Definir o Blueprint
alunos_bp = Blueprint('alunos', __name__)

@alunos_bp.route('/alunos', methods=['GET', 'POST'])
def alunos():
    """
    Gerenciar alunos (listar ou adicionar).
    """
    if request.method == 'GET':
        logger.info("Listando todos os alunos.")
        alunos = Aluno.query.all()
        return jsonify([
            {
                "id": aluno.id,
                "nome_completo": aluno.nome_completo,
                "data_nascimento": aluno.data_nascimento,
                "turma_id": aluno.turma_id
            } for aluno in alunos
        ]), 200

    if request.method == 'POST':
        pass

@alunos_bp.route('/alunos/<int:id>', methods=['GET'])
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

@alunos_bp.route('/alunos/<int:id>', methods=['PUT'])
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

@alunos_bp.route('/alunos/<int:id>', methods=['DELETE'])
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

@alunos_bp.route('/test-links', methods=['GET'])
def test_links():
    """
    Exibir links para testar os CRUDs no Insomnia.
    ---
    tags:
      - Test Links
    responses:
      200:
        description: Links para testar os CRUDs
        schema:
          type: object
          properties:
            links:
              type: array
              items:
                type: string
    """
    links = {
        "crudAluno": "/alunos",
        "crudAtividade_Aluno": "/atividade-aluno",
        "crudAtividade": "/atividades",
        "crudMatricula": "/matriculas",
        "crudNota": "/notas",
        "crudPagamento": "/pagamentos",
        "crudPresenca": "/presencas",
        "crudProfessor": "/professores",
        "crudTurma": "/turmas",
        "crudUsuario": "/usuarios"
    }
    return jsonify({"links": links}), 200

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)
