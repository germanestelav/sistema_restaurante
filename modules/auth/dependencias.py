from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from modules.auth.jwt_utils import verificar_token
from modules.usuarios.crud import get_usuario_por_username
from database.session import get_db
from sqlalchemy.orm import Session
from utils.logger import get_logger

logger = get_logger("modules.auth.dependencies")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    logger.info("Verificando token...")
    payload = verificar_token(token)
    if not payload:
        logger.warning("Token inválido o expirado")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    usuario = get_usuario_por_username(db, payload.get("sub"))
    logger.info(f"Token válido. Buscando usuario con username: {payload.get('sub')}")
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    logger.info(f"Usuario autenticado: {usuario.username}")
    return usuario