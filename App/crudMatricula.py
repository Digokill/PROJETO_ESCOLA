from flask import Flask, request, jsonify
from app import app, db
from models import Aluno, Turma
from logging_config import get_logger

logger = get_logger(__name__)

@app.route('/matriculas', methods=['POST'])
def criar_matricula():
    """
    Criar uma nova matrícula para um aluno em uma turma.
    """
    logger.info("Iniciando criação de matrícula.")
    data = request.get_json()
    try:
        aluno = Aluno.query.get(data['id_aluno'])
        turma = Turma.query.get(data['id_turma'])

        if not aluno:
            return jsonify({"error": "Aluno não encontrado"}), 404
        if not turma:
            return jsonify({"error": "Turma não encontrada"}), 404

        aluno.id_turma = data['id_turma']
        db.session.commit()
        logger.info(f"Matrícula do aluno {aluno.nome_completo} na turma {turma.nome_turma} realizada com sucesso.")
        return jsonify({"message": "Matrícula realizada com sucesso!"}), 201
    except Exception as e:
        logger.error(f"Erro ao criar matrícula: {e}")
        return jsonify({"error": str(e)}), 400

@app.route('/matriculas/<int:id_aluno>', methods=['GET'])
def consultar_matricula(id_aluno):
    """
    Consultar a matrícula de um aluno.
    """
    logger.info(f"Consultando matrícula do aluno com ID {id_aluno}.")
    aluno = Aluno.query.get(id_aluno)
    if aluno and aluno.id_turma:
        turma = Turma.query.get(aluno.id_turma)
        return jsonify({
            "id_aluno": aluno.id_aluno,
            "nome_aluno": aluno.nome_completo,
            "id_turma": turma.id_turma,
            "nome_turma": turma.nome_turma
        }), 200
    elif aluno:
        return jsonify({"message": "Aluno não está matriculado em nenhuma turma."}), 200
    else:
        return jsonify({"error": "Aluno não encontrado"}), 404

@app.route('/matriculas/<int:id_aluno>', methods=['PUT'])
def atualizar_matricula(id_aluno):
    """
    Atualizar a matrícula de um aluno para outra turma.
    """
    logger.info(f"Atualizando matrícula do aluno com ID {id_aluno}.")
    data = request.get_json()
    aluno = Aluno.query.get(id_aluno)
    turma = Turma.query.get(data['id_turma'])

    if not aluno:
        return jsonify({"error": "Aluno não encontrado"}), 404
    if not turma:
        return jsonify({"error": "Turma não encontrada"}), 404

    try:
        aluno.id_turma = data['id_turma']
        db.session.commit()
        logger.info(f"Matrícula do aluno {aluno.nome_completo} atualizada para a turma {turma.nome_turma}.")
        return jsonify({"message": "Matrícula atualizada com sucesso!"}), 200
    except Exception as e:
        logger.error(f"Erro ao atualizar matrícula: {e}")
        return jsonify({"error": str(e)}), 400

@app.route('/matriculas/<int:id_aluno>', methods=['DELETE'])
def deletar_matricula(id_aluno):
    """
    Remover a matrícula de um aluno.
    """
    logger.info(f"Removendo matrícula do aluno com ID {id_aluno}.")
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        return jsonify({"error": "Aluno não encontrado"}), 404

    try:
        aluno.id_turma = None
        db.session.commit()
        logger.info(f"Matrícula do aluno {aluno.nome_completo} removida com sucesso.")
        return jsonify({"message": "Matrícula removida com sucesso!"}), 200
    except Exception as e:
        logger.error(f"Erro ao remover matrícula: {e}")
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
