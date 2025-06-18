import psycopg2
from flask import Blueprint, request, jsonify
from logging_config import get_logger

logger = get_logger(__name__)

atividades_alunos_bp = Blueprint('atividades_alunos', __name__)

logger.info("CRUD AtividadeAluno iniciado com sucesso.")

def get_db_connection():
    return psycopg2.connect(
        dbname="escola",
        user="faat",
        password="faat",
        host="db",
        port=5432
    )

@atividades_alunos_bp.route('/atividades_alunos', methods=['GET', 'POST'])
def atividades_alunos():
    if request.method == 'GET':
        logger.info("Listando todas as relações de atividade e aluno.")
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT id_atividade, id_aluno FROM "Atividade_Aluno"')
            atividades_alunos = cur.fetchall()
            cur.close()
            conn.close()
            return jsonify([
                {
                    "id_atividade": a[0],
                    "id_aluno": a[1]
                } for a in atividades_alunos
            ]), 200
        except Exception as e:
            logger.error(f"Erro ao listar atividades_alunos: {e}")
            return jsonify({"error": str(e)}), 400
    if request.method == 'POST':
        logger.info("Iniciando registro de uma atividade para um aluno.")
        conn = get_db_connection()
        cur = conn.cursor()
        data = request.get_json()
        try:
            cur.execute(
                'INSERT INTO "Atividade_Aluno" (id_atividade, id_aluno) VALUES (%s, %s)',
                (data['id_atividade'], data['id_aluno'])
            )
            conn.commit()
            logger.info("Atividade do aluno registrada com sucesso.")
            return jsonify({'message': 'Atividade do aluno registrada com sucesso!'}), 201
        except Exception as e:
            logger.error(f"Erro ao registrar atividade do aluno: {e}")
            return jsonify({"error": str(e)}), 400
        finally:
            cur.close()
            conn.close()

@atividades_alunos_bp.route('/atividades_alunos/aluno/<int:id_aluno>', methods=['GET'])
def atividades_por_aluno(id_aluno):
    logger.info(f"Listando atividades do aluno {id_aluno}.")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_atividade, id_aluno FROM "Atividade_Aluno" WHERE id_aluno = %s', (id_aluno,))
        atividades = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {
                "id_atividade": a[0],
                "id_aluno": a[1]
            } for a in atividades
        ]), 200
    except Exception as e:
        logger.error(f"Erro ao listar atividades do aluno: {e}")
        return jsonify({"error": str(e)}), 400

@atividades_alunos_bp.route('/atividades_alunos/atividade/<int:id_atividade>', methods=['GET'])
def alunos_por_atividade(id_atividade):
    logger.info(f"Listando alunos da atividade {id_atividade}.")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_atividade, id_aluno FROM "Atividade_Aluno" WHERE id_atividade = %s', (id_atividade,))
        alunos = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {
                "id_atividade": a[0],
                "id_aluno": a[1]
            } for a in alunos
        ]), 200
    except Exception as e:
        logger.error(f"Erro ao listar alunos da atividade: {e}")
        return jsonify({"error": str(e)}), 400
