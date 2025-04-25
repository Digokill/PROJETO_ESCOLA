from flask import Flask, request, jsonify
import Util.bd as bd
import base64

from flask import request, jsonify
from app import app, db
from models import Turma

app = Flask(__name__)

@app.route('/turmas', methods=['POST'])
def add_turma():
    """
    Adicionar uma nova turma
    ---
    tags:
      - Turmas
    parameters:
      - in: body
        name: body
        required: true
        description: Dados da turma a ser adicionada
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "Turma A"
            professor_responsavel:
              type: string
              example: "Prof. João"
            horario:
              type: string
              example: "08:00 - 12:00"
    responses:
      201:
        description: Turma adicionada com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Turma adicionada com sucesso!"
      400:
        description: Erro na requisição
    """
    data = request.get_json()
    nova_turma = Turma(
        nome=data['nome'],
        professor_responsavel=data['professor_responsavel'],
        horario=data['horario']
    )
    db.session.add(nova_turma)
    db.session.commit()
    return jsonify({'message': 'Turma adicionada com sucesso!'}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
