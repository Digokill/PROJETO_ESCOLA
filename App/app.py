from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://faat:faat@postgres_db/escola'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configuração do Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/swagger/',
            "rule_filter": lambda rule: True,  # Todas as rotas
            "model_filter": lambda tag: True,  # Todos os modelos
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/"
}
swagger_template = {
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
    "host": "localhost:5000",  # Atualize conforme necessário
    "basePath": "/",  # Base da API
    "schemes": ["http"],
    "operationId": "getmyData",
    "consumes": ["application/json"],
    "produces": ["application/json"],
}
swagger = Swagger(app, config=swagger_config, template=swagger_template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)