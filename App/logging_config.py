import logging

def get_logger(name):
    logger = logging.getLogger(name) #Configurar o logger
    if not logger.hasHandlers(): #Verifica se o logger já possui handlers
        logger.setLevel(logging.DEBUG) #Nivel de B.O
        handler = logging.StreamHandler() #Fluxo de saída padrão (console)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler) #Adiciona o handler ao logger
    return logger
