from flask import Flask, request, jsonify
import Util.bd as bd
import base64

from flask import request, jsonify
from app import app, db
from models import Aluno, Turma, Pagamento, Presenca, Atividade

app = Flask(__name__)



@app.route('/atividades', methods=['POST'])
def add_atividade():
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
