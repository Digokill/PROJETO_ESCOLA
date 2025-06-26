import psycopg2 # conectar e interagir com bancos de dados PostgreSQL
from flask import Blueprint, request, jsonify
import bcrypt
from logging_config import get_logger #Alertas e logs

auth_bp = Blueprint('auth', __name__) #Nome e modulo do Blueprint (uma forma de organizar o código da API em partes menores. Assim, tudo relacionado à autenticação (login e cadastro) fica separado do resto do sistema.)
logger = get_logger(__name__)

def get_db_connection():
    return psycopg2.connect(
        dbname="escola",
        user="faat",
        password="faat",
        host="db",
        port=5432
    )

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    login = data.get('login')
    senha = data.get('senha')
    nivel_permissao = data.get('nivel_permissao', 'usuario')
    if not login or not senha:
        return jsonify({"error": "Login e senha são obrigatórios."}), 400
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO "Usuario" (login, senha, nivel_permissao) VALUES (%s, %s, %s)', (login, senha_hash, nivel_permissao))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Usuário registrado com sucesso!"}), 201
    except Exception as e:
        logger.error(f"Erro ao registrar usuário: {e}")
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    login = data.get('login')
    senha = data.get('senha')
    if not login or not senha:
        return jsonify({"error": "Login e senha são obrigatórios."}), 400
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT senha, nivel_permissao FROM "Usuario" WHERE login = %s', (login,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user and bcrypt.checkpw(senha.encode('utf-8'), user[0].encode('utf-8')):
            return jsonify({"message": "Login realizado com sucesso!", "nivel_permissao": user[1]}), 200
        else:
            return jsonify({"error": "Login ou senha inválidos."}), 401
    except Exception as e:
        logger.error(f"Erro ao fazer login: {e}")
        return jsonify({"error": str(e)}), 400
