from datetime import datetime, timedelta
from jose import JWTError, jwt
from utils.logger import get_logger

logger = get_logger("modules.auth.jwt_utils")

import os
SECRET_KEY = os.getenv("SECRET_KEY", "CAMBIA_ESTO_EN_PRODUCCION")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def crear_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"Token creado exitosamente con expiración: {expire}")
    return encoded_jwt

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info("Token verificado correctamente")
        return payload
    except JWTError as e:
        logger.warning(f"Error al verificar el token: {e}")
        return None