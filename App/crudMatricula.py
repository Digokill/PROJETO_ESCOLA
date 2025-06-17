import psycopg2
from flask import Blueprint, request, jsonify
from logging_config import get_logger

# Definir o Blueprint
matriculas_bp = Blueprint('matriculas', __name__)

logger = get_logger(__name__)

logger.info("CRUD Matricula iniciado com sucesso.")

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

@matriculas_bp.route('/matriculas', methods=['POST'])
def criar_matricula():
    """
    Criar uma nova matrícula para um aluno em uma turma.
    """
    logger.info("Iniciando criação de matrícula.")
    conn = get_db_connection()
    cur = conn.cursor()
    data = request.get_json()
    try:
        cur.execute(
            "UPDATE alunos SET turma_id = %s WHERE id = %s",
            (data['id_turma'], data['id_aluno'])
        )
        conn.commit()
        logger.info("Matrícula realizada com sucesso.")
        return jsonify({"message": "Matrícula realizada com sucesso!"}), 201
    except Exception as e:
        logger.error(f"Erro ao criar matrícula: {e}")
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

@matriculas_bp.route('/matriculas/<int:id_aluno>', methods=['GET'])
def consultar_matricula(id_aluno):
    """
    Consultar a matrícula de um aluno.
    """
    logger.info(f"Consultando matrícula do aluno com ID {id_aluno}.")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT turma_id FROM alunos WHERE id = %s", (id_aluno,))
    turma_id = cur.fetchone()
    cur.close()
    conn.close()
    if turma_id:
        return jsonify({"id_aluno": id_aluno, "turma_id": turma_id[0]}), 200
    else:
        return jsonify({"message": "Aluno não está matriculado em nenhuma turma."}), 200

@matriculas_bp.route('/matriculas/<int:id_aluno>', methods=['DELETE'])
def deletar_matricula(id_aluno):
    """
    Remover a matrícula de um aluno.
    """
    logger.info(f"Removendo matrícula do aluno com ID {id_aluno}.")
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE alunos SET turma_id = NULL WHERE id = %s", (id_aluno,))
        conn.commit()
        logger.info("Matrícula removida com sucesso.")
        return jsonify({"message": "Matrícula removida com sucesso!"}), 200
    except Exception as e:
        logger.error(f"Erro ao remover matrícula: {e}")
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()
