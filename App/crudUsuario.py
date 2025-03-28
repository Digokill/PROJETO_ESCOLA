from flask import Flask, request, jsonify
import Util.bd as bd
import base64

from flask import request, jsonify
from app import app, db
from models import Aluno, Turma, Pagamento, Presenca, Atividade, Usuario

app = Flask(__name__)

app.route('/usuarios', methods=['POST'])
def add_usuario():
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
