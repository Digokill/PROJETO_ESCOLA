import logging
from logging.handlers import RotatingFileHandler

# Configuração básica de logging
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "projeto_escola.log"

# Configurando o logger principal
logging.basicConfig(
    level=logging.DEBUG,
    format=LOG_FORMAT,
    handlers=[
        RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3),
        logging.StreamHandler()
    ]
)

# Função para obter loggers
def get_logger(name):
    return logging.getLogger(name)
