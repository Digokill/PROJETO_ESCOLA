from flask import Flask, request, jsonify
import Util.bd as bd
import base64

from flask import request, jsonify
from app import app, db
from models import Aluno, Turma, Pagamento, Presenca, Atividade

app = Flask(__name__)


@app.route('/pagamentos', methods=['POST'])
def add_pagamento():
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
