#Não usamos...
from logging_config import get_logger

logger = get_logger(__name__)

def autenticar_usuario(usuario, senha):
    logger.info(f"Tentativa de autenticação para o usuário: {usuario}")
    try:
        # Código de autenticação do usuário
        # Exemplo:
        if usuario == "admin" and senha == "1234":
            logger.info(f"Usuário {usuario} autenticado com sucesso.")
            return True
        else:
            raise ValueError("Credenciais inválidas")
    except Exception as e:
        logger.warning(f"Falha na autenticação para o usuário {usuario}: {e}")
        raise