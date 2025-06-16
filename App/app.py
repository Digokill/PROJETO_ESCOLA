from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter
import yaml
import socket
import time
import os

app = Flask(__name__)

 #Configuração do Prometheus
metrics = PrometheusMetrics(app, default_labels={'app_name': 'flask_app'})
success_counter = Counter(
    'http_success_count', 'Contagem de respostas HTTP com sucesso',
    ['endpoint', 'method', 'status']
)
error_counter = Counter(
    'http_error_count', 'Contagem de respostas HTTP com erro',
    ['endpoint', 'method', 'status']
)

@app.after_request
def after_request(response):
    """
    Middleware para capturar os retornos de todos os endpoints.
    """
    endpoint = request.path
    method = request.method
    status = response.status_code

    if 200 <= status < 300:
        success_counter.labels(endpoint=endpoint, method=method, status=str(status)).inc()
    else:
        error_counter.labels(endpoint=endpoint, method=method, status=str(status)).inc()

    return response

# Importar e registrar o Blueprint
from crudAluno import alunos_bp
app.register_blueprint(alunos_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
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

db_uri = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['name']}"

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do SQLAlchemy
db = SQLAlchemy()

# Inicializar o SQLAlchemy com o aplicativo Flask
db.init_app(app)

# Função para aguardar o banco de dados
def wait_for_db(host, port):
    with app.app_context():  # Adicionado para garantir o contexto do aplicativo
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

# Certifique-se de criar as tabelas dentro do contexto do aplicativo
with app.app_context():
    db.create_all()

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

from crudAluno import alunos_bp

# Registrar o Blueprint
app.register_blueprint(alunos_bp)

# # Importar o arquivo crudAluno para registrar as rotas
# import crudAluno

if __name__ == '__main__':
    with app.app_context():  # Adicionado para garantir o contexto do aplicativo
        app.run(host='0.0.0.0', port=5000, debug=True)