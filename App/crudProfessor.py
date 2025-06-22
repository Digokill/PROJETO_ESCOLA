import psycopg2
from flask import Flask, request, jsonify
from flask import Blueprint
from flasgger import Swagger
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter
from logging_config import get_logger
import bcrypt

logger = get_logger(__name__)

app = Flask(__name__)
swagger = Swagger(app)

# Configuração do Prometheus
metrics = PrometheusMetrics(app, default_labels={'app_name': 'flask_app'})

# Métricas personalizadas para sucessos e erros
success_counter = Counter(
    'http_success_count', 'Contagem de respostas HTTP com sucesso',
    ['endpoint', 'method', 'status']
)

error_counter = Counter(
    'http_error_count', 'Contagem de respostas HTTP com erro',
    ['endpoint', 'method', 'status']
)

@app.after_request
def after_request(response):
    """
    Middleware para capturar os retornos de todos os endpoints.
    """
    endpoint = request.path
    method = request.method
    status = response.status_code

    if 200 <= status < 300:
        success_counter.labels(endpoint=endpoint, method=method, status=str(status)).inc()
    else:
        error_counter.labels(endpoint=endpoint, method=method, status=str(status)).inc()

    return response

# Definir o Blueprint
professores_bp = Blueprint('professores', __name__)

logger.info("CRUD Professor iniciado com sucesso.")

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

@professores_bp.route('/professores', methods=['GET', 'POST'])
def professores():
    """
    Gerenciar professores (listar ou adicionar).
    """
    if request.method == 'GET':
        logger.info("Listando todos os professores.")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_professor, nome_completo, email, telefone FROM "Professor"')
        professores = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {
                "id_professor": professor[0],
                "nome_completo": professor[1],
                "email": professor[2],
                "telefone": professor[3]
            } for professor in professores
        ]), 200

    if request.method == 'POST':
        logger.info("Adicionando um novo professor.")
        data = request.get_json()

        # Verificar se os campos obrigatórios estão presentes
        if 'nome_completo' not in data or 'email' not in data or 'telefone' not in data or 'login' not in data or 'senha' not in data:
            logger.error("Campos obrigatórios ausentes na requisição.")
            return jsonify({"error": "Campos obrigatórios ausentes: 'nome_completo', 'email', 'telefone', 'login' e/ou 'senha'"}), 400

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            # Inserir professor
            cur.execute(
                'INSERT INTO "Professor" (nome_completo, email, telefone) VALUES (%s, %s, %s) RETURNING id_professor',
                (data['nome_completo'], data['email'], data['telefone'])
            )
            id_professor = cur.fetchone()[0]
            # Inserir usuário vinculado ao professor
            senha_hash = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())
            cur.execute(
                'INSERT INTO "Usuario" (login, senha, nivel_acesso, id_professor) VALUES (%s, %s, %s, %s)',
                (data['login'], senha_hash.decode('utf-8'), 'professor', id_professor)
            )
            conn.commit()
            cur.close()
            conn.close()
            logger.info("Professor e usuário criados com sucesso.")
            return jsonify({"message": "Professor e usuário criados com sucesso!", "id_professor": id_professor}), 201
        except Exception as e:
            logger.error(f"Erro ao adicionar professor: {e}")
            return jsonify({"error": str(e)}), 400

@professores_bp.route('/professor', methods=['GET', 'POST'])
def professor_alias():
    """
    Alias para o endpoint /professores.
    """
    return professores()

@professores_bp.route('/professores/<int:id>', methods=['GET'])
def ler_professor(id):
    """
    Endpoint para ler informações de um professor pelo ID.
    """
    logger.info(f"Lendo informações do professor com ID {id}.")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id_professor, nome_completo, email, telefone FROM "Professor" WHERE id_professor = %s', (id,))
    professor = cur.fetchone()
    cur.close()
    conn.close()
    if professor:
        return jsonify({
            "id_professor": professor[0],
            "nome_completo": professor[1],
            "email": professor[2],
            "telefone": professor[3]
        }), 200
    else:
        logger.error(f"Professor com ID {id} não encontrado.")
        return jsonify({"error": "Professor não encontrado"}), 404

@professores_bp.route('/professores/<int:id>', methods=['PUT'])
def atualizar_professor(id):
    """
    Endpoint para atualizar informações de um professor pelo ID.
    """
    logger.info(f"Atualizando informações do professor com ID {id}.")
    data = request.get_json()
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Atualiza dados do professor
        cur.execute(
            'UPDATE "Professor" SET nome_completo = %s, email = %s, telefone = %s WHERE id_professor = %s',
            (data.get('nome_completo'), data.get('email'), data.get('telefone'), id)
        )
        # Se senha for informada, atualiza também a senha do usuário vinculado
        if 'senha' in data and data['senha']:
            senha_hash = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())
            cur.execute(
                'UPDATE "Usuario" SET senha = %s WHERE id_professor = %s',
                (senha_hash.decode('utf-8'), id)
            )
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"Professor com ID {id} atualizado com sucesso.")
        return jsonify({"message": "Professor atualizado com sucesso!"}), 200
    except Exception as e:
        logger.error(f"Erro ao atualizar professor: {e}")
        return jsonify({"error": str(e)}), 400

@professores_bp.route('/professor/<int:id>', methods=['PUT'])
def atualizar_professor_alias(id):
    """
    Alias para o endpoint /professores/<id> para atualizar informações de um professor.
    """
    return atualizar_professor(id)

@professores_bp.route('/professores/<int:id>', methods=['DELETE'])
def deletar_professor(id):
    """
    Endpoint para deletar um professor pelo ID.
    """
    logger.info(f"Deletando professor com ID {id}.")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM "Professor" WHERE id_professor = %s', (id,))
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"Professor com ID {id} deletado com sucesso.")
        return jsonify({"message": "Professor deletado com sucesso!"}), 200
    except Exception as e:
        logger.error(f"Erro ao deletar professor: {e}")
        return jsonify({"error": str(e)}), 400

@professores_bp.route('/professor/<int:id>', methods=['DELETE'])
def deletar_professor_alias(id):
    """
    Alias para o endpoint /professores/<id> para deletar um professor.
    """
    return deletar_professor(id)

app.register_blueprint(professores_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# Exemplo de corpo JSON para criação de professor:
# {
#   "nome_completo": "João da Silva",
#   "email": "joao.silva@email.com",
#   "telefone": "(11) 91234-5678",
#   "disciplina": "Matemática",
#   "login": "joaosilva",
#   "senha": "senhaSegura123"
# }
