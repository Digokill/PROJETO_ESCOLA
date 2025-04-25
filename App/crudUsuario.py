from flask import Flask, request, jsonify
from flasgger import Swagger
import Util.bd as bd
import base64

from flask import request, jsonify
from app import app, db
from models import Usuario

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/usuarios', methods=['POST'])
def add_usuario():
    """
    Adicionar um novo usuário
    ---
    tags:
      - Usuários
    parameters:
      - in: body
        name: body
        required: true
        description: Dados do usuário a ser adicionado
        schema:
          type: object
          properties:
            nome_usuario:
              type: string
              example: "admin"
            senha:
              type: string
              example: "123456"
            tipo_usuario:
              type: string
              example: "administrador"
    responses:
      201:
        description: Usuário adicionado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Usuário adicionado com sucesso!"
      400:
        description: Erro na requisição
    """
    data = request.get_json()
    novo_usuario = Usuario(
        nome_usuario=data['nome_usuario'],
        senha=data['senha'],
        tipo_usuario=data['tipo_usuario']
    )
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({'message': 'Usuário adicionado com sucesso!'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
