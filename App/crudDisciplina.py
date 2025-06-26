import psycopg2
from flask import Blueprint, request, jsonify
from logging_config import get_logger

logger = get_logger(__name__)

disciplinas_bp = Blueprint('disciplinas', __name__)

logger.info("CRUD Disciplina iniciado com sucesso.")

def get_db_connection():
    return psycopg2.connect(
        dbname="escola",
        user="faat",
        password="faat",
        host="db",
        port=5432
    )

@disciplinas_bp.route('/disciplinas', methods=['GET', 'POST'])
def disciplinas():
    if request.method == 'GET':
        logger.info("Listando todas as disciplinas.")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_disciplina, nome_disciplina, codigo, carga_horaria FROM "Disciplina"')
        disciplinas = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {
                "id_disciplina": d[0],
                "nome_disciplina": d[1],
                "codigo": d[2],
                "carga_horaria": d[3]
            } for d in disciplinas
        ]), 200

    if request.method == 'POST':
        logger.info("Adicionando uma nova disciplina.")
        data = request.get_json()
        if 'nome_disciplina' not in data or 'codigo' not in data or 'carga_horaria' not in data:
            logger.error("Campos obrigatórios ausentes na requisição.")
            return jsonify({"error": "Campos obrigatórios ausentes: 'nome_disciplina', 'codigo' e/ou 'carga_horaria'"}), 400
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO "Disciplina" (nome_disciplina, codigo, carga_horaria) VALUES (%s, %s, %s)',
                (data['nome_disciplina'], data['codigo'], data['carga_horaria'])
            )
            conn.commit()
            cur.close()
            conn.close()
            logger.info("Disciplina adicionada com sucesso.")
            return jsonify({"message": "Disciplina adicionada com sucesso!"}), 201
        except Exception as e:
            logger.error(f"Erro ao adicionar disciplina: {e}")
            return jsonify({"error": str(e)}), 400

@disciplinas_bp.route('/disciplina', methods=['GET', 'POST'])
def disciplina_alias():
    return disciplinas()

@disciplinas_bp.route('/disciplinas/<int:id>', methods=['GET'])
def ler_disciplina(id):
    logger.info(f"Lendo informações da disciplina com ID {id}.")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id_disciplina, nome_disciplina, codigo, carga_horaria FROM "Disciplina" WHERE id_disciplina = %s', (id,))
    d = cur.fetchone()
    cur.close()
    conn.close()
    if d:
        return jsonify({
            "id_disciplina": d[0],
            "nome_disciplina": d[1],
            "codigo": d[2],
            "carga_horaria": d[3]
        }), 200
    else:
        logger.error(f"Disciplina com ID {id} não encontrada.")
        return jsonify({"error": "Disciplina não encontrada"}), 404

@disciplinas_bp.route('/disciplinas/<int:id>', methods=['PUT'])
def atualizar_disciplina(id):
    logger.info(f"Atualizando informações da disciplina com ID {id}.")
    data = request.get_json()
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'UPDATE "Disciplina" SET nome_disciplina = %s, codigo = %s, carga_horaria = %s WHERE id_disciplina = %s',
            (data.get('nome_disciplina'), data.get('codigo'), data.get('carga_horaria'), id)
        )
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"Disciplina com ID {id} atualizada com sucesso.")
        return jsonify({"message": "Disciplina atualizada com sucesso!"}), 200
    except Exception as e:
        logger.error(f"Erro ao atualizar disciplina: {e}")
        return jsonify({"error": str(e)}), 400

@disciplinas_bp.route('/disciplina/<int:id>', methods=['PUT'])
def atualizar_disciplina_alias(id):
    return atualizar_disciplina(id)#Permite usar outro nome para o endpoint, como /disciplina/<id> (Alias)

@disciplinas_bp.route('/disciplinas/<int:id>', methods=['DELETE'])
def deletar_disciplina(id):
    logger.info(f"Deletando disciplina com ID {id}.")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM "Disciplina" WHERE id_disciplina = %s', (id,))
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"Disciplina com ID {id} deletada com sucesso.")
        return jsonify({"message": "Disciplina deletada com sucesso!"}), 200
    except Exception as e:
        logger.error(f"Erro ao deletar disciplina: {e}")
        return jsonify({"error": str(e)}), 400

@disciplinas_bp.route('/disciplina/<int:id>', methods=['DELETE'])
def deletar_disciplina_alias(id):
    return deletar_disciplina(id)
