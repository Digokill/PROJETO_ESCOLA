import psycopg2
from flask import Blueprint, request, jsonify
from logging_config import get_logger

# Definir o Blueprint
alunos_bp = Blueprint('alunos', __name__)

logger = get_logger(__name__)

logger.info("CRUD Aluno iniciado com sucesso.")

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

@alunos_bp.route('/alunos', methods=['GET', 'POST'])
def alunos():
    """
    Gerenciar alunos (listar ou adicionar).
    """
    if request.method == 'GET':
        logger.info("Listando todos os alunos.")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nome_completo, data_nascimento, turma_id FROM alunos")
        alunos = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {
                "id": aluno[0],
                "nome_completo": aluno[1],
                "data_nascimento": aluno[2],
                "turma_id": aluno[3]
            } for aluno in alunos
        ]), 200

    if request.method == 'POST':
        logger.info("Adicionando um novo aluno.")
        data = request.get_json()
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO alunos (nome_completo, data_nascimento, turma_id) VALUES (%s, %s, %s)",
                (data['nome_completo'], data['data_nascimento'], data['turma_id'])
            )
            conn.commit()
            cur.close()
            conn.close()
            logger.info("Aluno adicionado com sucesso.")
            return jsonify({"message": "Aluno adicionado com sucesso!"}), 201
        except Exception as e:
            logger.error(f"Erro ao adicionar aluno: {e}")
            return jsonify({"error": str(e)}), 400

@alunos_bp.route('/alunos/<int:id>', methods=['GET'])
def ler_aluno(id):
    """
    Endpoint para ler informações de um aluno pelo ID.
    """
    logger.info(f"Lendo informações do aluno com ID {id}.")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome_completo, data_nascimento, turma_id FROM alunos WHERE id = %s", (id,))
    aluno = cur.fetchone()
    cur.close()
    conn.close()
    if aluno:
        return jsonify({
            "id": aluno[0],
            "nome_completo": aluno[1],
            "data_nascimento": aluno[2],
            "turma_id": aluno[3]
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
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE alunos SET nome_completo = %s, data_nascimento = %s, turma_id = %s WHERE id = %s",
            (data.get('nome_completo'), data.get('data_nascimento'), data.get('turma_id'), id)
        )
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"Aluno com ID {id} atualizado com sucesso.")
        return jsonify({"message": "Aluno atualizado com sucesso!"}), 200
    except Exception as e:
        logger.error(f"Erro ao atualizar aluno: {e}")
        return jsonify({"error": str(e)}), 400

@alunos_bp.route('/alunos/<int:id>', methods=['DELETE'])
def deletar_aluno(id):
    """
    Endpoint para deletar um aluno pelo ID.
    """
    logger.info(f"Deletando aluno com ID {id}.")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM alunos WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"Aluno com ID {id} deletado com sucesso.")
        return jsonify({"message": "Aluno deletado com sucesso!"}), 200
    except Exception as e:
        logger.error(f"Erro ao deletar aluno: {e}")
        return jsonify({"error": str(e)}), 400

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
