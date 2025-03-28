from flask import Flask, request, jsonify
import Util.bd as bd
import base64

from flask import request, jsonify
from app import app, db
from models import Aluno, Turma, Pagamento, Presenca, Atividade, AtividadeAluno

app = Flask(__name__)

app.route('/atividades_alunos', methods=['POST'])
def add_atividade_aluno():
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
