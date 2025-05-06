from logging_config import get_logger

logger = get_logger(__name__)

def criar_registro(dados):
    logger.info("Iniciando criação de registro.")
    try:
        # Código para criar registro
        logger.info("Registro criado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao criar registro: {e}")
        raise

def ler_registro(id):
    logger.info(f"Lendo registro com ID: {id}")
    try:
        # Código para ler registro
        logger.info(f"Registro com ID {id} lido com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao ler registro com ID {id}: {e}")
        raise

def atualizar_registro(id, novos_dados):
    logger.info(f"Iniciando atualização do registro com ID: {id}")
    try:
        # Código para atualizar registro
        logger.info(f"Registro com ID {id} atualizado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao atualizar registro com ID {id}: {e}")
        raise

def deletar_registro(id):
    logger.info(f"Iniciando exclusão do registro com ID: {id}")
    try:
        # Código para deletar registro
        logger.info(f"Registro com ID {id} excluído com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao excluir registro com ID {id}: {e}")
        raise