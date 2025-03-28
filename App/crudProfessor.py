from flask import Flask, request, jsonify
import Util.bd as bd
import base64

from flask import request, jsonify
from app import app, db
from models import Aluno, Turma, Pagamento, Presenca, Atividade, Professor

app = Flask(__name__)

@app.route('/professores', methods=['POST'])
def add_professor():
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
