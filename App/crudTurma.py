import psycopg2
from flask import Blueprint, request, jsonify
from logging_config import get_logger

logger = get_logger(__name__)

turmas_bp = Blueprint('turmas', __name__)

logger.info("CRUD Turma iniciado com sucesso.")

def get_db_connection():
    return psycopg2.connect(
        dbname="escola",
        user="faat",
        password="faat",
        host="db",
        port=5432
    )

@turmas_bp.route('/turmas', methods=['GET', 'POST'])
def turmas():
    if request.method == 'GET':
        logger.info("Listando todas as turmas.")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_turma, nome_turma, id_professor, horario, ano_letivo, id_disciplina FROM "Turma"')
        turmas = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {
                "id_turma": turma[0],
                "nome_turma": turma[1],
                "id_professor": turma[2],
                "horario": turma[3],
                "ano_letivo": turma[4],
                "id_disciplina": turma[5]
            } for turma in turmas
        ]), 200

    if request.method == 'POST':
        logger.info("Adicionando uma nova turma.")
        data = request.get_json()
        if 'nome_turma' not in data or 'id_professor' not in data or 'horario' not in data:
            logger.error("Campos obrigatórios ausentes na requisição.")
            return jsonify({"error": "Campos obrigatórios ausentes: 'nome_turma', 'id_professor' e/ou 'horario'"}), 400
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO "Turma" (nome_turma, id_professor, horario, ano_letivo, id_disciplina) VALUES (%s, %s, %s, %s, %s)',
                (data['nome_turma'], data['id_professor'], data['horario'], data.get('ano_letivo'), data.get('id_disciplina'))
            )
            conn.commit()
            cur.close()
            conn.close()
            logger.info("Turma adicionada com sucesso.")
            return jsonify({"message": "Turma adicionada com sucesso!"}), 201
        except Exception as e:
            logger.error(f"Erro ao adicionar turma: {e}")
            return jsonify({"error": str(e)}), 400

@turmas_bp.route('/turma', methods=['GET', 'POST'])
def turma_alias():
    return turmas()

@turmas_bp.route('/turmas/<int:id>', methods=['GET'])
def ler_turma(id):
    logger.info(f"Lendo informações da turma com ID {id}.")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id_turma, nome_turma, id_professor, horario, ano_letivo, id_disciplina FROM "Turma" WHERE id_turma = %s', (id,))
    turma = cur.fetchone()
    cur.close()
    conn.close()
    if turma:
        return jsonify({
            "id_turma": turma[0],
            "nome_turma": turma[1],
            "id_professor": turma[2],
            "horario": turma[3],
            "ano_letivo": turma[4],
            "id_disciplina": turma[5]
        }), 200
    else:
        logger.error(f"Turma com ID {id} não encontrada.")
        return jsonify({"error": "Turma não encontrada"}), 404

@turmas_bp.route('/turmas/<int:id>', methods=['PUT'])
def atualizar_turma(id):
    logger.info(f"Atualizando informações da turma com ID {id}.")
    data = request.get_json()
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'UPDATE "Turma" SET nome_turma = %s, id_professor = %s, horario = %s, ano_letivo = %s, id_disciplina = %s WHERE id_turma = %s',
            (data.get('nome_turma'), data.get('id_professor'), data.get('horario'), data.get('ano_letivo'), data.get('id_disciplina'), id)
        )
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"Turma com ID {id} atualizada com sucesso.")
        return jsonify({"message": "Turma atualizada com sucesso!"}), 200
    except Exception as e:
        logger.error(f"Erro ao atualizar turma: {e}")
        return jsonify({"error": str(e)}), 400

@turmas_bp.route('/turma/<int:id>', methods=['PUT'])
def atualizar_turma_alias(id):
    return atualizar_turma(id)

@turmas_bp.route('/turmas/<int:id>', methods=['DELETE'])
def deletar_turma(id):
    logger.info(f"Deletando turma com ID {id}.")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM "Turma" WHERE id_turma = %s', (id,))
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"Turma com ID {id} deletada com sucesso.")
        return jsonify({"message": "Turma deletada com sucesso!"}), 200
    except Exception as e:
        logger.error(f"Erro ao deletar turma: {e}")
        return jsonify({"error": str(e)}), 400

@turmas_bp.route('/turma/<int:id>', methods=['DELETE'])
def deletar_turma_alias(id):
    return deletar_turma(id)

@turmas_bp.route('/turmas/professor/<int:id_professor>', methods=['GET'])
def turmas_por_professor(id_professor):
    logger.info(f"Listando turmas do professor {id_professor}.")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_turma, nome_turma, id_professor, horario, ano_letivo, id_disciplina FROM "Turma" WHERE id_professor = %s', (id_professor,))
        turmas = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {
                "id_turma": t[0],
                "nome_turma": t[1],
                "id_professor": t[2],
                "horario": t[3],
                "ano_letivo": t[4],
                "id_disciplina": t[5]
            } for t in turmas
        ]), 200
    except Exception as e:
        logger.error(f"Erro ao listar turmas do professor: {e}")
        return jsonify({"error": str(e)}), 400

@turmas_bp.route('/turmas/<int:id_turma>', methods=['GET'])
def turma_por_id(id_turma):
    logger.info(f"Buscando turma com id {id_turma}.")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_turma, nome_turma, id_professor, horario, ano_letivo, id_disciplina FROM "Turma" WHERE id_turma = %s', (id_turma,))
        turma = cur.fetchone()
        cur.close()
        conn.close()
        if turma:
            return jsonify({
                "id_turma": turma[0],
                "nome_turma": turma[1],
                "id_professor": turma[2],
                "horario": turma[3],
                "ano_letivo": turma[4],
                "id_disciplina": turma[5]
            }), 200
        else:
            return jsonify({"error": "Turma não encontrada"}), 404
    except Exception as e:
        logger.error(f"Erro ao buscar turma por id: {e}")
        return jsonify({"error": str(e)}), 400

@turmas_bp.route('/turmas/horario/<horario>', methods=['GET'])
def turmas_por_horario(horario):
    logger.info(f"Listando turmas com horário {horario}.")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_turma, nome_turma, id_professor, horario, ano_letivo, id_disciplina FROM "Turma" WHERE horario = %s', (horario,))
        turmas = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {
                "id_turma": t[0],
                "nome_turma": t[1],
                "id_professor": t[2],
                "horario": t[3],
                "ano_letivo": t[4],
                "id_disciplina": t[5]
            } for t in turmas
        ]), 200
    except Exception as e:
        logger.error(f"Erro ao listar turmas por horário: {e}")
        return jsonify({"error": str(e)}), 400
