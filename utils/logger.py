import logging

def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.FileHandler("app.log")  # Cambia el nombre si quieres otro archivo
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger