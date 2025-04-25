from flask import Flask, request, jsonify
import Util.bd as bd
import base64

from flask import request, jsonify
from app import app, db
from models import Aluno, Turma, Pagamento, Presenca, Atividade, AtividadeAluno
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/atividades_alunos', methods=['POST'])
def add_atividade_aluno():
    """
    Registrar uma atividade para um aluno
    ---
    tags:
      - Atividades Alunos
    parameters:
      - in: body
        name: body
        required: true
        description: Dados da atividade do aluno a ser registrada
        schema:
          type: object
          properties:
            aluno_id:
              type: integer
              example: 1
            atividade_id:
              type: integer
              example: 2
            nota:
              type: number
              format: float
              example: 9.5
    responses:
      201:
        description: Atividade do aluno registrada com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Atividade do aluno registrada com sucesso!"
      400:
        description: Erro na requisição
    """
    data = request.get_json()
    nova_atividade_aluno = AtividadeAluno(
        aluno_id=data['aluno_id'],
        atividade_id=data['atividade_id'],
        nota=data['nota']
    )
    db.session.add(nova_atividade_aluno)
    db.session.commit()
    return jsonify({'message': 'Atividade do aluno registrada com sucesso!'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
