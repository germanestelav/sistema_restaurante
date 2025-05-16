from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from modules.auth.jwt_utils import verificar_token
from modules.usuarios.crud import get_usuario_por_username
from database.session import get_db
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verificar_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    usuario = get_usuario_por_username(db, payload.get("sub"))
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario