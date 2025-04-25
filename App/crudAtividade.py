from flask import Flask, request, jsonify
import Util.bd as bd
import base64

from flask import request, jsonify
from app import app, db
from models import  Atividade
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/atividades', methods=['POST'])
def add_atividade():
    """
    Cadastrar uma nova atividade
    ---
    tags:
      - Atividades
    parameters:
      - in: body
        name: body
        required: true
        description: Dados da atividade a ser cadastrada
        schema:
          type: object
          properties:
            descricao:
              type: string
              example: "Prova de Matemática"
            data_realizacao:
              type: string
              format: date
              example: "2023-10-15"
            turma_id:
              type: integer
              example: 1
    responses:
      201:
        description: Atividade cadastrada com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Atividade cadastrada com sucesso!"
      400:
        description: Erro na requisição
    """
    data = request.get_json()
    nova_atividade = Atividade(
        descricao=data['descricao'],
        data_realizacao=data['data_realizacao'],
        turma_id=data['turma_id']
    )
    db.session.add(nova_atividade)
    db.session.commit()
    return jsonify({'message': 'Atividade cadastrada com sucesso!'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
