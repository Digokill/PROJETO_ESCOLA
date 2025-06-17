from flask import Flask, request
from flasgger import Swagger
import yaml
import socket
import time
import os

app = Flask(__name__)

# Carregar configurações do arquivo config.yaml
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

db_config = config['database']

# Detectar se está dentro do Docker
# if os.getenv('DOCKER_ENV') == 'true':
#     db_config['host'] = 'db'
#     db_config['port'] = 5432
# else:
#     db_config['host'] = 'localhost'
#     db_config['port'] = 3001

# Função para aguardar o banco de dados
def wait_for_db(host, port):
    while True:
        try:
            with socket.create_connection((host, port), timeout=2):
                print("Database is ready!")
                break
        except (socket.timeout, ConnectionRefusedError):
            print("Waiting for the database...")
            time.sleep(2)

# Esperar pelo banco de dados antes de inicializar o Flask
wait_for_db(db_config['host'], db_config['port'])

# Configuração do Swagger
swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "API Escola Infantil",
        "description": "Documentação da API para o sistema de gestão de escola infantil.",
        "version": "1.0.0",
        "contact": {
            "responsibleOrganization": "Escola Infantil",
            "responsibleDeveloper": "Equipe de Desenvolvimento",
            "email": "contato@escola.com",
            "url": "http://escola.com",
        },
    },
    "host": "localhost:5000",
    "basePath": "/",
    "schemes": ["http"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
})

# Importar o blueprint após a inicialização do aplicativo
from crudAluno import alunos_bp

# Registrar o Blueprint
app.register_blueprint(alunos_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)