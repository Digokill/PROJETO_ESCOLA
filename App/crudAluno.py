import psycopg2
from flask import Blueprint, request, jsonify, send_file
from logging_config import get_logger
import pandas as pd

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

@alunos_bp.route('/alunos/nome/<nome_completo>', methods=['GET'])
def buscar_aluno_por_nome(nome_completo):
    """
    Endpoint para buscar alunos pelo nome completo.
    """
    logger.info(f"Buscando alunos com nome_completo: {nome_completo}")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_aluno, nome_completo, data_nascimento, id_turma, informacoes_adicionais, email_responsavel, telefone_responsavel, nome_responsavel FROM "Alunos" WHERE nome_completo = %s', (nome_completo,))
        alunos = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {
                "id_aluno": a[0],
                "nome_completo": a[1],
                "data_nascimento": a[2],
                "id_turma": a[3],
                "informacoes_adicionais": a[4],
                "email_responsavel": a[5],
                "telefone_responsavel": a[6],
                "nome_responsavel": a[7]
            } for a in alunos
        ]), 200
    except Exception as e:
        logger.error(f"Erro ao buscar aluno por nome: {e}")
        return jsonify({"error": str(e)}), 400

@alunos_bp.route('/alunos/id/<int:id_aluno>', methods=['GET'])
def buscar_aluno_por_id(id_aluno):
    """
    Endpoint para buscar um aluno pelo ID.
    """
    logger.info(f"Buscando aluno com id_aluno: {id_aluno}")
    try:
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
            return jsonify({"error": "Aluno não encontrado"}), 404
    except Exception as e:
        logger.error(f"Erro ao buscar aluno por id: {e}")
        return jsonify({"error": str(e)}), 400

@alunos_bp.route('/alunos/responsavel/<nome_responsavel>', methods=['GET'])
def buscar_aluno_por_responsavel(nome_responsavel):
    """
    Endpoint para buscar alunos pelo nome do responsável.
    """
    logger.info(f"Buscando alunos com nome_responsavel: {nome_responsavel}")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_aluno, nome_completo, data_nascimento, id_turma, informacoes_adicionais, email_responsavel, telefone_responsavel, nome_responsavel FROM "Alunos" WHERE nome_responsavel = %s', (nome_responsavel,))
        alunos = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {
                "id_aluno": a[0],
                "nome_completo": a[1],
                "data_nascimento": a[2],
                "id_turma": a[3],
                "informacoes_adicionais": a[4],
                "email_responsavel": a[5],
                "telefone_responsavel": a[6],
                "nome_responsavel": a[7]
            } for a in alunos
        ]), 200
    except Exception as e:
        logger.error(f"Erro ao buscar aluno por nome_responsavel: {e}")
        return jsonify({"error": str(e)}), 400

@alunos_bp.route('/alunos/data_nascimento/<data_nascimento>', methods=['GET'])
def buscar_aluno_por_data_nascimento(data_nascimento):
    """
    Endpoint para buscar alunos pela data de nascimento.
    """
    logger.info(f"Buscando alunos com data_nascimento: {data_nascimento}")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_aluno, nome_completo, data_nascimento, id_turma, informacoes_adicionais, email_responsavel, telefone_responsavel, nome_responsavel FROM "Alunos" WHERE data_nascimento = %s', (data_nascimento,))
        alunos = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {
                "id_aluno": a[0],
                "nome_completo": a[1],
                "data_nascimento": a[2],
                "id_turma": a[3],
                "informacoes_adicionais": a[4],
                "email_responsavel": a[5],
                "telefone_responsavel": a[6],
                "nome_responsavel": a[7]
            } for a in alunos
        ]), 200
    except Exception as e:
        logger.error(f"Erro ao buscar aluno por data_nascimento: {e}")
        return jsonify({"error": str(e)}), 400

@alunos_bp.route('/alunos/exportar_excel', methods=['GET'])
def exportar_alunos_excel():
    """
    Endpoint para exportar relatório de alunos em Excel.
    """
    logger.info("Exportando relatório de alunos para Excel.")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_aluno, nome_completo, data_nascimento, id_turma, informacoes_adicionais, email_responsavel, telefone_responsavel, nome_responsavel FROM "Alunos"')
        alunos = cur.fetchall()
        columns = ["id_aluno", "nome_completo", "data_nascimento", "id_turma", "informacoes_adicionais", "email_responsavel", "telefone_responsavel", "nome_responsavel"]
        df = pd.DataFrame(alunos, columns=columns)
        file_path = "alunos_relatorio.xlsx"
        df.to_excel(file_path, index=False)
        cur.close()
        conn.close()
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        logger.error(f"Erro ao exportar alunos para Excel: {e}")
        return jsonify({"error": str(e)}), 400
