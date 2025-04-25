from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://faat:faat@postgres_db/escola'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)