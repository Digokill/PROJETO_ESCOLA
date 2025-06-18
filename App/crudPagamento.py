import psycopg2
from flask import Blueprint, request, jsonify
from logging_config import get_logger

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
            cur.execute('SELECT id_pagamento, id_aluno, data_pagamento, valor_pago, forma_pagamento, referencia, status FROM "Pagamento"')
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
                    "status": p[6]
                } for p in pagamentos
            ]), 200
        except Exception as e:
            logger.error(f"Erro ao listar pagamentos: {e}")
            return jsonify({"error": str(e)}), 400
    if request.method == 'POST':
        logger.info("Registrando pagamento.")
        data = request.get_json()
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO "Pagamento" (id_aluno, data_pagamento, valor_pago, forma_pagamento, referencia, status) VALUES (%s, %s, %s, %s, %s, %s)',
                (data['id_aluno'], data['data_pagamento'], data['valor_pago'], data['forma_pagamento'], data['referencia'], data['status'])
            )
            conn.commit()
            cur.close()
            conn.close()
            logger.info("Pagamento registrado com sucesso.")
            return jsonify({"message": "Pagamento registrado com sucesso!"}), 201
        except Exception as e:
            logger.error(f"Erro ao registrar pagamento: {e}")
            return jsonify({"error": str(e)}), 400

@pagamentos_bp.route('/pagamentos/<int:id_aluno>', methods=['GET'])
def consultar_pagamentos(id_aluno):
    logger.info(f"Consultando pagamentos do aluno {id_aluno}.")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_pagamento, data_pagamento, valor_pago, forma_pagamento, referencia, status FROM "Pagamento" WHERE id_aluno = %s', (id_aluno,))
        pagamentos = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {
                "id_pagamento": p[0],
                "data_pagamento": p[1],
                "valor_pago": p[2],
                "forma_pagamento": p[3],
                "referencia": p[4],
                "status": p[5]
            } for p in pagamentos
        ]), 200
    except Exception as e:
        logger.error(f"Erro ao consultar pagamentos: {e}")
        return jsonify({"error": str(e)}), 400
