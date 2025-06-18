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

@usuarios_bp.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    if request.method == 'GET':
        logger.info("Listando todos os usuários.")
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT id_usuario, login, senha, nivel_acesso, id_professor FROM "Usuario"')
            usuarios = cur.fetchall()
            cur.close()
            conn.close()
            return jsonify([
                {
                    "id_usuario": u[0],
                    "login": u[1],
                    "senha": u[2],
                    "nivel_acesso": u[3],
                    "id_professor": u[4]
                } for u in usuarios
            ]), 200
        except Exception as e:
            logger.error(f"Erro ao listar usuários: {e}")
            return jsonify({"error": str(e)}), 400
    if request.method == 'POST':
        return add_usuario()

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
            'INSERT INTO "Usuario" (login, senha, nivel_acesso, id_professor) VALUES (%s, %s, %s, %s)',
            (data['login'], data['senha'], data['nivel_acesso'], data.get('id_professor'))
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

@usuarios_bp.route('/usuarios/login/<login>', methods=['GET'])
def buscar_usuario_por_login(login):
    logger.info(f"Buscando usuário com login: {login}")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_usuario, login, senha, nivel_acesso, id_professor FROM "Usuario" WHERE login = %s', (login,))
        usuario = cur.fetchone()
        cur.close()
        conn.close()
        if usuario:
            return jsonify({
                "id_usuario": usuario[0],
                "login": usuario[1],
                "senha": usuario[2],
                "nivel_acesso": usuario[3],
                "id_professor": usuario[4]
            }), 200
        else:
            return jsonify({"error": "Usuário não encontrado"}), 404
    except Exception as e:
        logger.error(f"Erro ao buscar usuário por login: {e}")
        return jsonify({"error": str(e)}), 400
