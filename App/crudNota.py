from flask import Flask, request, jsonify
from app import app, db
from models import Nota, Aluno, Disciplina
from logging_config import get_logger

logger = get_logger(__name__)

@app.route('/notas', methods=['POST'])
def registrar_nota():
    """
    Registrar uma nova nota para um aluno em uma disciplina.
    """
    logger.info("Iniciando registro de nota.")
    data = request.get_json()
    try:
        aluno = Aluno.query.get(data['id_aluno'])
        disciplina = Disciplina.query.get(data['id_disciplina'])

        if not aluno:
            return jsonify({"error": "Aluno não encontrado"}), 404
        if not disciplina:
            return jsonify({"error": "Disciplina não encontrada"}), 404

        nova_nota = Nota(
            id_aluno=data['id_aluno'],
            id_disciplina=data['id_disciplina'],
            nota=data['nota'],
            data_lancamento=data['data_lancamento']
        )
        db.session.add(nova_nota)
        db.session.commit()
        logger.info(f"Nota registrada para o aluno {aluno.nome_completo} na disciplina {disciplina.nome_disciplina}.")
        return jsonify({"message": "Nota registrada com sucesso!"}), 201
    except Exception as e:
        logger.error(f"Erro ao registrar nota: {e}")
        return jsonify({"error": str(e)}), 400

@app.route('/notas/<int:id_aluno>', methods=['GET'])
def consultar_notas(id_aluno):
    """
    Consultar as notas de um aluno.
    """
    logger.info(f"Consultando notas do aluno com ID {id_aluno}.")
    notas = Nota.query.filter_by(id_aluno=id_aluno).all()
    if notas:
        return jsonify([{
            "id_nota": nota.id_nota,
            "id_disciplina": nota.id_disciplina,
            "nota": nota.nota,
            "data_lancamento": nota.data_lancamento
        } for nota in notas]), 200
    else:
        return jsonify({"message": "Nenhuma nota encontrada para o aluno."}), 200

@app.route('/notas/<int:id_nota>', methods=['PUT'])
def atualizar_nota(id_nota):
    """
    Atualizar uma nota existente.
    """
    logger.info(f"Atualizando nota com ID {id_nota}.")
    data = request.get_json()
    nota = Nota.query.get(id_nota)
    if not nota:
        return jsonify({"error": "Nota não encontrada"}), 404

    try:
        nota.nota = data.get('nota', nota.nota)
        nota.data_lancamento = data.get('data_lancamento', nota.data_lancamento)
        db.session.commit()
        logger.info(f"Nota com ID {id_nota} atualizada com sucesso.")
        return jsonify({"message": "Nota atualizada com sucesso!"}), 200
    except Exception as e:
        logger.error(f"Erro ao atualizar nota: {e}")
        return jsonify({"error": str(e)}), 400

@app.route('/notas/<int:id_nota>', methods=['DELETE'])
def deletar_nota(id_nota):
    """
    Deletar uma nota.
    """
    logger.info(f"Deletando nota com ID {id_nota}.")
    nota = Nota.query.get(id_nota)
    if not nota:
        return jsonify({"error": "Nota não encontrada"}), 404

    try:
        db.session.delete(nota)
        db.session.commit()
        logger.info(f"Nota com ID {id_nota} deletada com sucesso.")
        return jsonify({"message": "Nota deletada com sucesso!"}), 200
    except Exception as e:
        logger.error(f"Erro ao deletar nota: {e}")
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
