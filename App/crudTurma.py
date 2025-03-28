from flask import Flask, request, jsonify
import Util.bd as bd
import base64

from flask import request, jsonify
from app import app, db
from models import Aluno, Turma, Pagamento, Presenca, Atividade

app = Flask(__name__)



@app.route('/turmas', methods=['POST'])
def add_turma():
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
