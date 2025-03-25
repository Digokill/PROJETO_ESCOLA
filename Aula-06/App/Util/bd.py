import psycopg2
from psycopg2 import OperationalError
import yaml

with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

def create_connection():
    """"
    Create a connection to the PostgreSQL database."
    :return: Connection object or None
    """
    connection = None
    try:
        connection = psycopg2.connect(
            user=config['user'],
            password=config['password'],
            host=config['host'],
            port=config['port'],
            database=config['database']
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection