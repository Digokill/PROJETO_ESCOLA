import psycopg2
from flask import Blueprint, request, jsonify, send_file
from logging_config import get_logger
import pandas as pd

logger = get_logger(__name__)

pagamentos_bp = Blueprint('pagamentos', __name__)

logger.info("CRUD Pagamento iniciado com sucesso.")

def get_db_connection():
    return psycopg2.connect(
        dbname="escola",
        user="faat",
        password="faat",
        host="db",
        port=5432
    )

@pagamentos_bp.route('/pagamentos', methods=['GET', 'POST'])
def pagamentos():
    if request.method == 'GET':
        logger.info("Listando todos os pagamentos.")
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT id_pagamento, id_aluno, data_pagamento, valor_pago, forma_pagamento, referencia, status, vencimento FROM "Pagamento"')
            pagamentos = cur.fetchall()
            cur.close()
            conn.close()
            return jsonify([
                {
                    "id_pagamento": p[0],
                    "id_aluno": p[1],
                    "data_pagamento": p[2],
                    "valor_pago": p[3],
                    "forma_pagamento": p[4],
                    "referencia": p[5],
                    "status": p[6],
                    "vencimento": p[7]
                } for p in pagamentos
            ]), 200
        except Exception as e:
            logger.error(f"Erro ao listar pagamentos: {e}")
            return jsonify({"error": str(e)}), 400
    if request.method == 'POST':
        logger.info("Registrando pagamento.")
        data = request.get_json()
        try:
            status = data.get('status', '').lower()
            if status == 'pendente':
                data_pagamento = None
            else:
                data_pagamento = data.get('data_pagamento')
                if not data_pagamento:
                    return jsonify({"error": "Campo 'data_pagamento' é obrigatório para pagamentos não pendentes."}), 400
            vencimento = data.get('vencimento')
            if not vencimento or str(vencimento).strip() == '':
                vencimento = None
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO "Pagamento" (id_aluno, data_pagamento, valor_pago, forma_pagamento, referencia, status, vencimento) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (
                    data['id_aluno'],
                    data_pagamento,
                    data.get('valor_pago'),
                    data.get('forma_pagamento'),
                    data.get('referencia'),
                    data['status'],
                    vencimento
                )
            )
            conn.commit()
            cur.close()
            conn.close()
            logger.info("Pagamento registrado com sucesso.")
            return jsonify({"message": "Pagamento registrado com sucesso!"}), 201
        except Exception as e:
            logger.error(f"Erro ao registrar pagamento: {e}")
            return jsonify({"error": str(e)}), 400

@pagamentos_bp.route('/pagamentos/aluno/<int:id_aluno>', methods=['GET'])
def pagamentos_por_aluno(id_aluno):
    logger.info(f"Listando pagamentos do aluno {id_aluno}.")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_pagamento, id_aluno, data_pagamento, valor_pago, forma_pagamento, referencia, status, vencimento FROM "Pagamento" WHERE id_aluno = %s', (id_aluno,))
        pagamentos = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {
                "id_pagamento": p[0],
                "id_aluno": p[1],
                "data_pagamento": p[2],
                "valor_pago": p[3],
                "forma_pagamento": p[4],
                "referencia": p[5],
                "status": p[6],
                "vencimento": p[7]
            } for p in pagamentos
        ]), 200
    except Exception as e:
        logger.error(f"Erro ao listar pagamentos do aluno: {e}")
        return jsonify({"error": str(e)}), 400

@pagamentos_bp.route('/pagamentos/status/<status>', methods=['GET'])
def pagamentos_por_status(status):
    logger.info(f"Listando pagamentos com status {status}.")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_pagamento, id_aluno, data_pagamento, valor_pago, forma_pagamento, referencia, status, vencimento FROM "Pagamento" WHERE status = %s', (status,))
        pagamentos = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {
                "id_pagamento": p[0],
                "id_aluno": p[1],
                "data_pagamento": p[2],
                "valor_pago": p[3],
                "forma_pagamento": p[4],
                "referencia": p[5],
                "status": p[6],
                "vencimento": p[7]
            } for p in pagamentos
        ]), 200
    except Exception as e:
        logger.error(f"Erro ao listar pagamentos por status: {e}")
        return jsonify({"error": str(e)}), 400

@pagamentos_bp.route('/pagamentos/exportar_excel', methods=['GET'])
def exportar_pagamentos_excel():
    logger.info("Exportando relatório de pagamentos para Excel.")
    try:
        data_inicial = request.args.get('data_inicial')
        data_final = request.args.get('data_final')
        conn = get_db_connection()
        cur = conn.cursor()
        query = '''
            SELECT p.id_pagamento, a.nome_completo, p.id_aluno, p.data_pagamento, p.valor_pago, p.forma_pagamento, p.referencia, p.status, p.vencimento
            FROM "Pagamento" p
            JOIN "Alunos" a ON p.id_aluno = a.id_aluno
        '''
        params = []
        if data_inicial and data_final:
            query += ' WHERE p.data_pagamento BETWEEN %s AND %s'
            params = [data_inicial, data_final]
        cur.execute(query, params)
        pagamentos = cur.fetchall()
        columns = ["id_pagamento", "nome_completo", "id_aluno", "data_pagamento", "valor_pago", "forma_pagamento", "referencia", "status", "vencimento"]
        df = pd.DataFrame(pagamentos, columns=columns)
        df['inadimplente'] = df['status'].apply(lambda x: x.lower() == 'pendente')
        file_path = "pagamentos_relatorio.xlsx"
        df.to_excel(file_path, index=False)
        cur.close()
        conn.close()
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        logger.error(f"Erro ao exportar pagamentos para Excel: {e}")
        return jsonify({"error": str(e)}), 400
