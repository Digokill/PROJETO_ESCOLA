import psycopg2
from flask import Blueprint, request, jsonify
from logging_config import get_logger

# Definir o Blueprint
alunos_bp = Blueprint('alunos', __name__)

logger = get_logger(__name__)

logger.info("CRUD Aluno iniciado com sucesso.")

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

@alunos_bp.route('/alunos', methods=['GET', 'POST'])
def alunos():
    """
    Gerenciar alunos (listar ou adicionar).
    """
    if request.method == 'GET':
        logger.info("Listando todos os alunos.")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_aluno, nome_completo, data_nascimento, id_turma, informacoes_adicionais, email_responsavel, telefone_responsavel, nome_responsavel FROM "Alunos"')
        alunos = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {
                "id_aluno": aluno[0],
                "nome_completo": aluno[1],
                "data_nascimento": aluno[2],
                "id_turma": aluno[3],
                "informacoes_adicionais": aluno[4],
                "email_responsavel": aluno[5],
                "telefone_responsavel": aluno[6],
                "nome_responsavel": aluno[7]
            } for aluno in alunos
        ]), 200

    if request.method == 'POST':
        logger.info("Adicionando um novo aluno.")
        data = request.get_json()
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO "Alunos" (nome_completo, data_nascimento, id_turma, informacoes_adicionais, email_responsavel, telefone_responsavel, nome_responsavel) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (
                    data['nome_completo'],
                    data['data_nascimento'],
                    data['id_turma'],
                    data.get('informacoes_adicionais'),
                    data.get('email_responsavel'),
                    data.get('telefone_responsavel'),
                    data.get('nome_responsavel')
                )
            )
            conn.commit()
            cur.close()
            conn.close()
            logger.info("Aluno adicionado com sucesso.")
            return jsonify({"message": "Aluno adicionado com sucesso!"}), 201
        except Exception as e:
            logger.error(f"Erro ao adicionar aluno: {e}")
            return jsonify({"error": str(e)}), 400

@alunos_bp.route('/alunos/<int:id_aluno>', methods=['GET'])
def ler_aluno(id_aluno):
    """
    Endpoint para ler informações de um aluno pelo ID.
    """
    logger.info(f"Lendo informações do aluno com ID {id_aluno}.")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id_aluno, nome_completo, data_nascimento, id_turma, informacoes_adicionais, email_responsavel, telefone_responsavel, nome_responsavel FROM "Alunos" WHERE id_aluno = %s', (id_aluno,))
    aluno = cur.fetchone()
    cur.close()
    conn.close()
    if aluno:
        return jsonify({
            "id_aluno": aluno[0],
            "nome_completo": aluno[1],
            "data_nascimento": aluno[2],
            "id_turma": aluno[3],
            "informacoes_adicionais": aluno[4],
            "email_responsavel": aluno[5],
            "telefone_responsavel": aluno[6],
            "nome_responsavel": aluno[7]
        }), 200
    else:
        logger.error(f"Aluno com ID {id_aluno} não encontrado.")
        return jsonify({"error": "Aluno não encontrado"}), 404

@alunos_bp.route('/alunos/<int:id_aluno>', methods=['PUT'])
def atualizar_aluno(id_aluno):
    """
    Endpoint para atualizar informações de um aluno pelo ID.
    """
    logger.info(f"Atualizando informações do aluno com ID {id_aluno}.")
    data = request.get_json()
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'UPDATE "Alunos" SET nome_completo = %s, data_nascimento = %s, id_turma = %s, informacoes_adicionais = %s, email_responsavel = %s, telefone_responsavel = %s, nome_responsavel = %s WHERE id_aluno = %s',
            (
                data.get('nome_completo'),
                data.get('data_nascimento'),
                data.get('id_turma'),
                data.get('informacoes_adicionais'),
                data.get('email_responsavel'),
                data.get('telefone_responsavel'),
                data.get('nome_responsavel'),
                id_aluno
            )
        )
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"Aluno com ID {id_aluno} atualizado com sucesso.")
        return jsonify({"message": "Aluno atualizado com sucesso!"}), 200
    except Exception as e:
        logger.error(f"Erro ao atualizar aluno: {e}")
        return jsonify({"error": str(e)}), 400

@alunos_bp.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def deletar_aluno(id_aluno):
    """
    Endpoint para deletar um aluno pelo ID.
    """
    logger.info(f"Deletando aluno com ID {id_aluno}.")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM "Alunos" WHERE id_aluno = %s', (id_aluno,))
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"Aluno com ID {id_aluno} deletado com sucesso.")
        return jsonify({"message": "Aluno deletado com sucesso!"}), 200
    except Exception as e:
        logger.error(f"Erro ao deletar aluno: {e}")
        return jsonify({"error": str(e)}), 400

@alunos_bp.route('/test-links', methods=['GET'])
def test_links():
    """
    Exibir links para testar os CRUDs no Insomnia.
    ---
    tags:
      - Test Links
    responses:
      200:
        description: Links para testar os CRUDs
        schema:
          type: object
          properties:
            links:
              type: array
              items:
                type: string
    """
    links = {
        "crudAluno": "/alunos",
        "crudAtividade_Aluno": "/atividade-aluno",
        "crudAtividade": "/atividades",
        "crudMatricula": "/matriculas",
        "crudNota": "/notas",
        "crudPagamento": "/pagamentos",
        "crudPresenca": "/presencas",
        "crudProfessor": "/professores",
        "crudTurma": "/turmas",
        "crudUsuario": "/usuarios"
    }
    return jsonify({"links": links}), 200
