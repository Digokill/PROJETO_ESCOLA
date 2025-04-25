from flask import Flask, request, jsonify
import Util.bd as bd
import base64

from flask import request, jsonify
from app import app, db
from models import Professor
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/professores', methods=['POST'])
def add_professor():
    """
    Adicionar um novo professor
    ---
    tags:
      - Professores
    parameters:
      - in: body
        name: body
        required: true
        description: Dados do professor a ser adicionado
        schema:
          type: object
          properties:
            nome_completo:
              type: string
              example: "Maria Silva"
            especialidade:
              type: string
              example: "Matemática"
            turma_id:
              type: integer
              example: 1
    responses:
      201:
        description: Professor adicionado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Professor adicionado com sucesso!"
      400:
        description: Erro na requisição
    """
    data = request.get_json()
    novo_professor = Professor(
        nome_completo=data['nome_completo'],
        especialidade=data['especialidade'],
        turma_id=data['turma_id']
    )
    db.session.add(novo_professor)
    db.session.commit()
    return jsonify({'message': 'Professor adicionado com sucesso!'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
