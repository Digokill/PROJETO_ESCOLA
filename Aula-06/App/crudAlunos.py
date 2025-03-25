from flask import Flask, request, jsonify
import Util.bd as bd
import base64

app = Flask(__name__)

@app.route('/alunos', methods=['POST'])
def adicionar_aluno():
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO alunos (aluno_id, nome, endereco, cidade, estado, cep, pais, telefone)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (data['aluno_id'], data['nome'], data['endereco'], data['cidade'], data['estado'], data['cep'], data['pais'], data['telefone'])
        )
        conn.commit()
        return jsonify({"message": "Aluno adicionado"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos/<int:aluno_id', methods=['GET'])
def read_aluno(aluno_id):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM alunos WHERE aluno_id = %s
            """,
            (aluno_id,)
        )
        aluno = cursor.fetchone()
        if aluno is None:
            return jsonify({"error": "Aluno não encontrado"}), 404
        return jsonify({
            "aluno_id": aluno[0],
            "nome": aluno[1],
            "endereco": aluno[2],
            "cidade": aluno[3],
            "estado": aluno[4],
            "cep": aluno[5],
            "pais": aluno[6],
            "telefone": aluno[7]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos/<int:aluno_id>', methods=['PUT'])
def update_aluno(aluno_id):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE alunos
            SET nome = %s, endereco = %s, cidade = %s, estado = %s, cep = %s, pais = %s, telefone = %s
            WHERE aluno_id = %s
            """,
            (data['nome'], data['endereco'], data['cidade'], data['estado'], data['cep'], data['pais'], data['telefone'], aluno_id)
        )
        conn.commit()
        return jsonify({"message": "Aluno atualizado"}), 200
    except Exception as e:  
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos/<int:aluno_id>', methods=['DELETE'])
def delete_aluno(aluno_id):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM alunos WHERE aluno_id = %s
            """,
            (aluno_id,)
        )
        conn.commit()
        return jsonify({"message": "Aluno deletado"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
