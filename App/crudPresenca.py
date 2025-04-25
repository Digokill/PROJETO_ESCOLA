from flask import Flask, request, jsonify
from flasgger import Swagger
import Util.bd as bd
import base64

from flask import request, jsonify
from app import app, db
from models import  Presenca

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/presencas', methods=['POST'])
def add_presenca():
    """
    Registrar uma nova presença
    ---
    tags:
      - Presenças
    parameters:
      - in: body
        name: body
        required: true
        description: Dados da presença a ser registrada
        schema:
          type: object
          properties:
            aluno_id:
              type: integer
              example: 1
            data:
              type: string
              format: date
              example: "2023-10-01"
            presente:
              type: boolean
              example: true
    responses:
      201:
        description: Presença registrada com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Presença registrada com sucesso!"
      400:
        description: Erro na requisição
    """
    data = request.get_json()
    nova_presenca = Presenca(
        aluno_id=data['aluno_id'],
        data=data['data'],
        presente=data['presente']
    )
    db.session.add(nova_presenca)
    db.session.commit()
    return jsonify({'message': 'Presença registrada com sucesso!'}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
