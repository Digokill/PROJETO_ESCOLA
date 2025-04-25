from flask import Flask, request, jsonify
import Util.bd as bd
import base64

from flask import request, jsonify
from app import app, db
from models import Pagamento
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)


@app.route('/pagamentos', methods=['POST'])
def add_pagamento():
    """
    Registrar um novo pagamento
    ---
    tags:
      - Pagamentos
    parameters:
      - in: body
        name: body
        required: true
        description: Dados do pagamento a ser registrado
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
            valor_pago:
              type: number
              format: float
              example: 150.50
            forma_pagamento:
              type: string
              example: "Cartão de Crédito"
    responses:
      201:
        description: Pagamento registrado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Pagamento registrado com sucesso!"
      400:
        description: Erro na requisição
    """
    data = request.get_json()
    novo_pagamento = Pagamento(
        aluno_id=data['aluno_id'],
        data=data['data'],
        valor_pago=data['valor_pago'],
        forma_pagamento=data['forma_pagamento']
    )
    db.session.add(novo_pagamento)
    db.session.commit()
    return jsonify({'message': 'Pagamento registrado com sucesso!'}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
