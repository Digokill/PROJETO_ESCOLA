from flask import Flask, request, jsonify
import Util.bd as bd
import base64

from flask import request, jsonify
from app import app, db
from models import Aluno

app = Flask(__name__)

@app.route('/alunos', methods=['POST'])
def add_aluno():
    """
    Adicionar um novo aluno
    ---
    tags:
      - Alunos
    parameters:
      - in: body
        name: body
        required: true
        description: Dados do aluno a ser adicionado
        schema:
          type: object
          properties:
            nome_completo:
              type: string
              example: "João Silva"
            data_nascimento:
              type: string
              format: date
              example: "2010-05-15"
            turma_id:
              type: integer
              example: 1
    responses:
      201:
        description: Aluno adicionado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Aluno adicionado com sucesso!"
      400:
        description: Erro na requisição
    """
    data = request.get_json()
    novo_aluno = Aluno(
        nome_completo=data['nome_completo'],
        data_nascimento=data['data_nascimento'],
        turma_id=data['turma_id']
    )
    db.session.add(novo_aluno)
    db.session.commit()
    return jsonify({'message': 'Aluno adicionado com sucesso!'}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
