import psycopg2
from flask import Blueprint, request, jsonify
from logging_config import get_logger

# Definir o Blueprint
notas_bp = Blueprint('notas', __name__)

logger = get_logger(__name__)

logger.info("CRUD Nota iniciado com sucesso.")

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

@notas_bp.route('/notas', methods=['GET', 'POST'])
def notas():
    if request.method == 'GET':
        logger.info("Listando todas as notas.")
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT id_nota, id_aluno, id_disciplina, nota, data_lancamento FROM "Nota"')
            notas = cur.fetchall()
            cur.close()
            conn.close()
            return jsonify([
                {
                    "id_nota": n[0],
                    "id_aluno": n[1],
                    "id_disciplina": n[2],
                    "nota": n[3],
                    "data_lancamento": n[4]
                } for n in notas
            ]), 200
        except Exception as e:
            logger.error(f"Erro ao listar notas: {e}")
            return jsonify({"error": str(e)}), 400
    if request.method == 'POST':
        return registrar_nota()

@notas_bp.route('/notas/<int:id_aluno>', methods=['GET'])
def consultar_notas(id_aluno):
    """
    Consultar as notas de um aluno.
    """
    logger.info(f"Consultando notas do aluno com ID {id_aluno}.")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id_nota, id_disciplina, nota, data_lancamento FROM "Nota" WHERE id_aluno = %s', (id_aluno,))
    notas = cur.fetchall()
    cur.close()
    conn.close()
    if notas:
        return jsonify([{
            "id_nota": nota[0],
            "id_disciplina": nota[1],
            "nota": nota[2],
            "data_lancamento": nota[3]
        } for nota in notas]), 200
    else:
        return jsonify({"message": "Nenhuma nota encontrada para o aluno."}), 200

@notas_bp.route('/notas/<int:id_nota>', methods=['PUT'])
def atualizar_nota(id_nota):
    """
    Atualizar uma nota existente.
    """
    logger.info(f"Atualizando nota com ID {id_nota}.")
    conn = get_db_connection()
    cur = conn.cursor()
    data = request.get_json()
    try:
        cur.execute(
            'UPDATE "Nota" SET nota = %s, data_lancamento = %s WHERE id_nota = %s',
            (data.get('nota'), data.get('data_lancamento'), id_nota)
        )
        conn.commit()
        logger.info("Nota atualizada com sucesso.")
        return jsonify({"message": "Nota atualizada com sucesso!"}), 200
    except Exception as e:
        logger.error(f"Erro ao atualizar nota: {e}")
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

@notas_bp.route('/notas/<int:id_nota>', methods=['DELETE'])
def deletar_nota(id_nota):
    """
    Deletar uma nota.
    """
    logger.info(f"Deletando nota com ID {id_nota}.")
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM "Nota" WHERE id_nota = %s', (id_nota,))
        conn.commit()
        logger.info("Nota deletada com sucesso.")
        return jsonify({"message": "Nota deletada com sucesso!"}), 200
    except Exception as e:
        logger.error(f"Erro ao deletar nota: {e}")
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()
