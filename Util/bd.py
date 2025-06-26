#Apenas para importar o arquivo de configuração do banco de dados (config.yaml) e obter as credenciais do banco de dados.
import os
import yaml

config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')

with open(config_path, 'r') as config_file:
    config = yaml.safe_load(config_file)

# Database configuration
database_config = config['database']
host = database_config['host']
port = database_config['port']
user = database_config['user']
password = database_config['password']
name = database_config['name']