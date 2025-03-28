from flask import Flask, request, jsonify
import Util.bd as bd
import base64

from flask import request, jsonify
from app import app, db
from models import Aluno, Turma, Pagamento, Presenca, Atividade

app = Flask(__name__)



@app.route('/presencas', methods=['POST'])
def add_presenca():
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
