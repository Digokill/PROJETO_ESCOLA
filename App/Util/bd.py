import psycopg2
from psycopg2 import OperationalError
import yaml
import os

config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')

try:
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)['database']
except (yaml.YAMLError, KeyError) as e:
    print(f"Error loading YAML configuration: {e}")
    config = None

def create_connection():
    """"Create a connection to the PostgreSQL database."
    :return: Connection object or None
    """
    if not config:
        print("Database configuration is missing or invalid.")
        return None

    connection = None
    try:
        connection = psycopg2.connect(
            user=config['user'],
            password=config['password'],
            host=config['host'],
            port=config['port'],
            database=config['name']
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection