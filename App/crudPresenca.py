import psycopg2
from flask import Blueprint, request, jsonify, send_file
from logging_config import get_logger
import pandas as pd

logger = get_logger(__name__)

presencas_bp = Blueprint('presencas', __name__)

logger.info("CRUD Presenca iniciado com sucesso.")

def get_db_connection():
    return psycopg2.connect(
        dbname="escola",
        user="faat",
        password="faat",
        host="db",
        port=5432
    )

# Exemplo de endpoint para registrar presença
@presencas_bp.route('/presencas', methods=['POST'])
def registrar_presenca():
    logger.info("Registrando presença.")
    data = request.get_json()
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO "Presenca" (id_aluno, data_presenca, presente) VALUES (%s, %s, %s)',
            (data['id_aluno'], data['data_presenca'], data['presente'])
        )
        conn.commit()
        cur.close()
        conn.close()
        logger.info("Presença registrada com sucesso.")
        return jsonify({"message": "Presença registrada com sucesso!"}), 201
    except Exception as e:
        logger.error(f"Erro ao registrar presença: {e}")
        return jsonify({"error": str(e)}), 400

# Exemplo de endpoint para consultar presença de um aluno
@presencas_bp.route('/presencas/<int:id_aluno>', methods=['GET'])
def consultar_presenca(id_aluno):
    logger.info(f"Consultando presenças do aluno {id_aluno}.")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_presenca, data_presenca, presente FROM "Presenca" WHERE id_aluno = %s', (id_aluno,))
        presencas = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {
                "id_presenca": p[0],
                "data_presenca": p[1],
                "presente": p[2]
            } for p in presencas
        ]), 200
    except Exception as e:
        logger.error(f"Erro ao consultar presenças: {e}")
        return jsonify({"error": str(e)}), 400

@presencas_bp.route('/presencas', methods=['GET', 'POST'])
def presencas():
    if request.method == 'GET':
        logger.info("Listando todas as presenças.")
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT id_presenca, id_aluno, data_presenca, presente FROM "Presenca"')
            presencas = cur.fetchall()
            cur.close()
            conn.close()
            return jsonify([
                {
                    "id_presenca": p[0],
                    "id_aluno": p[1],
                    "data_presenca": p[2],
                    "presente": p[3]
                } for p in presencas
            ]), 200
        except Exception as e:
            logger.error(f"Erro ao listar presenças: {e}")
            return jsonify({"error": str(e)}), 400
    if request.method == 'POST':
        logger.info("Registrando presença.")
        data = request.get_json()
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO "Presenca" (id_aluno, data_presenca, presente) VALUES (%s, %s, %s)',
                (data['id_aluno'], data['data_presenca'], data['presente'])
            )
            conn.commit()
            cur.close()
            conn.close()
            logger.info("Presença registrada com sucesso.")
            return jsonify({"message": "Presença registrada com sucesso!"}), 201
        except Exception as e:
            logger.error(f"Erro ao registrar presença: {e}")
            return jsonify({"error": str(e)}), 400

@presencas_bp.route('/presencas/aluno/<int:id_aluno>', methods=['GET'])
def presencas_por_aluno(id_aluno):
    logger.info(f"Listando presenças do aluno {id_aluno}.")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_presenca, id_aluno, data_presenca, presente FROM "Presenca" WHERE id_aluno = %s', (id_aluno,))
        presencas = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {
                "id_presenca": p[0],
                "id_aluno": p[1],
                "data_presenca": p[2],
                "presente": p[3]
            } for p in presencas
        ]), 200
    except Exception as e:
        logger.error(f"Erro ao listar presenças do aluno: {e}")
        return jsonify({"error": str(e)}), 400

@presencas_bp.route('/presencas/data/<data_presenca>', methods=['GET'])
def presencas_por_data(data_presenca):
    logger.info(f"Listando presenças na data {data_presenca}.")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_presenca, id_aluno, data_presenca, presente FROM "Presenca" WHERE data_presenca = %s', (data_presenca,))
        presencas = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {
                "id_presenca": p[0],
                "id_aluno": p[1],
                "data_presenca": p[2],
                "presente": p[3]
            } for p in presencas
        ]), 200
    except Exception as e:
        logger.error(f"Erro ao listar presenças por data: {e}")
        return jsonify({"error": str(e)}), 400

@presencas_bp.route('/presencas/exportar_excel', methods=['GET'])
def exportar_presencas_excel():
    logger.info("Exportando relatório de presenças para Excel com frequência semanal e mensal e nome do aluno.")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT p.id_aluno, a.nome_completo, p.data_presenca, p.presente
            FROM "Presenca" p
            JOIN "Alunos" a ON p.id_aluno = a.id_aluno
        ''')
        presencas = cur.fetchall()
        columns = ["id_aluno", "nome_completo", "data_presenca", "presente"]
        df = pd.DataFrame(presencas, columns=columns)
        df['data_presenca'] = pd.to_datetime(df['data_presenca'])
        df_presentes = df[df['presente'] == True]
        # Total de presenças por aluno
        total_presencas = df_presentes.groupby(['id_aluno', 'nome_completo']).size().rename('total_presencas')
        # Frequência semanal por aluno
        freq_semanal = df_presentes.groupby(['id_aluno', 'nome_completo', df_presentes['data_presenca'].dt.isocalendar().week]).size().groupby(['id_aluno', 'nome_completo']).mean().rename('frequencia_semanal')
        # Frequência mensal por aluno
        freq_mensal = df_presentes.groupby(['id_aluno', 'nome_completo', df_presentes['data_presenca'].dt.month]).size().groupby(['id_aluno', 'nome_completo']).mean().rename('frequencia_mensal')
        # Junta tudo em um DataFrame
        relatorio = pd.concat([total_presencas, freq_semanal, freq_mensal], axis=1).reset_index()
        file_path = "presencas_relatorio.xlsx"
        relatorio.to_excel(file_path, index=False)
        cur.close()
        conn.close()
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        logger.error(f"Erro ao exportar presenças para Excel: {e}")
        return jsonify({"error": str(e)}), 400
