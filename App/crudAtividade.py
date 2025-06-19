import psycopg2
from flask import Blueprint, request, jsonify
from logging_config import get_logger

logger = get_logger(__name__)

atividades_bp = Blueprint('atividades', __name__)

logger.info("CRUD Atividade iniciado com sucesso.")

def get_db_connection():
    return psycopg2.connect(
        dbname="escola",
        user="faat",
        password="faat",
        host="db",
        port=5432
    )

@atividades_bp.route('/atividades', methods=['GET', 'POST'])
def atividades():
    if request.method == 'GET':
        logger.info("Listando todas as atividades.")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT a.id_atividade, a.descricao, a.data_realizacao, a.id_turma, t.nome_turma
            FROM "Atividade" a
            LEFT JOIN "Turma" t ON a.id_turma = t.id_turma
        ''')
        atividades = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {
                "id_atividade": a[0],
                "descricao": a[1],
                "data_realizacao": a[2],
                "id_turma": a[3],
                "nome_turma": a[4]
            } for a in atividades
        ]), 200
    if request.method == 'POST':
        logger.info("Adicionando uma nova atividade.")
        data = request.get_json()
        if 'nome_turma' not in data:
            logger.error("Campo obrigatório 'nome_turma' não informado.")
            return jsonify({"error": "Campo obrigatório 'nome_turma' não informado."}), 400
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            # Buscar id_turma pelo nome_turma
            cur.execute('SELECT id_turma FROM "Turma" WHERE nome_turma = %s', (data['nome_turma'],))
            turma = cur.fetchone()
            if not turma:
                cur.close()
                conn.close()
                logger.error("Turma não encontrada.")
                return jsonify({"error": "Turma não encontrada."}), 400
            id_turma = turma[0]
            cur.execute(
                'INSERT INTO "Atividade" (descricao, data_realizacao, id_turma) VALUES (%s, %s, %s)',
                (data['descricao'], data['data_realizacao'], id_turma)
            )
            conn.commit()
            cur.close()
            conn.close()
            logger.info("Atividade adicionada com sucesso.")
            return jsonify({"message": "Atividade adicionada com sucesso!"}), 201
        except Exception as e:
            logger.error(f"Erro ao adicionar atividade: {e}")
            return jsonify({"error": str(e)}), 400

@atividades_bp.route('/atividades/<int:id>', methods=['GET'])
def ler_atividade(id):
    logger.info(f"Lendo informações da atividade com ID {id}.")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id_atividade, descricao, data_realizacao FROM "Atividade" WHERE id_atividade = %s', (id,))
    a = cur.fetchone()
    cur.close()
    conn.close()
    if a:
        return jsonify({
            "id_atividade": a[0],
            "descricao": a[1],
            "data_realizacao": a[2]
        }), 200
    else:
        logger.error(f"Atividade com ID {id} não encontrada.")
        return jsonify({"error": "Atividade não encontrada"}), 404

@atividades_bp.route('/atividades/<int:id>', methods=['PUT'])
def atualizar_atividade(id):
    logger.info(f"Atualizando informações da atividade com ID {id}.")
    data = request.get_json()
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'UPDATE "Atividade" SET descricao = %s, data_realizacao = %s WHERE id_atividade = %s',
            (data.get('descricao'), data.get('data_realizacao'), id)
        )
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"Atividade com ID {id} atualizada com sucesso.")
        return jsonify({"message": "Atividade atualizada com sucesso!"}), 200
    except Exception as e:
        logger.error(f"Erro ao atualizar atividade: {e}")
        return jsonify({"error": str(e)}), 400

@atividades_bp.route('/atividades/<int:id>', methods=['DELETE'])
def deletar_atividade(id):
    logger.info(f"Deletando atividade com ID {id}.")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM "Atividade" WHERE id_atividade = %s', (id,))
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"Atividade com ID {id} deletada com sucesso.")
        return jsonify({"message": "Atividade deletada com sucesso!"}), 200
    except Exception as e:
        logger.error(f"Erro ao deletar atividade: {e}")
        return jsonify({"error": str(e)}), 400

@atividades_bp.route('/atividades/aluno/<nome_aluno>', methods=['GET'])
def atividades_por_nome_aluno(nome_aluno):
    logger.info(f"Listando atividades para o aluno {nome_aluno}.")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Buscar a turma do aluno
        cur.execute('SELECT t.id_turma FROM "Alunos" a JOIN "Turma" t ON a.id_turma = t.id_turma WHERE a.nome_completo = %s', (nome_aluno,))
        turma = cur.fetchone()
        if not turma:
            cur.close()
            conn.close()
            logger.error("Aluno ou turma não encontrada.")
            return jsonify({"error": "Aluno ou turma não encontrada."}), 404
        id_turma = turma[0]
        # Buscar atividades da turma
        cur.execute('''
            SELECT a.id_atividade, a.descricao, a.data_realizacao, a.id_turma, t.nome_turma
            FROM "Atividade" a
            LEFT JOIN "Turma" t ON a.id_turma = t.id_turma
            WHERE a.id_turma = %s
        ''', (id_turma,))
        atividades = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {
                "id_atividade": a[0],
                "descricao": a[1],
                "data_realizacao": a[2],
                "id_turma": a[3],
                "nome_turma": a[4]
            } for a in atividades
        ]), 200
    except Exception as e:
        logger.error(f"Erro ao buscar atividades por nome do aluno: {e}")
        return jsonify({"error": str(e)}), 400
