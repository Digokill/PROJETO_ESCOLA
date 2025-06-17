import psycopg2
from flask import Blueprint, request, jsonify
from logging_config import get_logger

# Definir o Blueprint
usuarios_bp = Blueprint('usuarios', __name__)

logger = get_logger(__name__)

logger.info("CRUD Usuario iniciado com sucesso.")

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

@usuarios_bp.route('/usuarios', methods=['POST'])
def add_usuario():
    """
    Adicionar um novo usuário.
    """
    logger.info("Iniciando adição de um novo usuário.")
    conn = get_db_connection()
    cur = conn.cursor()
    data = request.get_json()
    try:
        cur.execute(
            "INSERT INTO usuarios (nome_usuario, senha, tipo_usuario) VALUES (%s, %s, %s)",
            (data['nome_usuario'], data['senha'], data['tipo_usuario'])
        )
        conn.commit()
        logger.info("Usuário adicionado com sucesso.")
        return jsonify({'message': 'Usuário adicionado com sucesso!'}), 201
    except Exception as e:
        logger.error(f"Erro ao adicionar usuário: {e}")
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()
