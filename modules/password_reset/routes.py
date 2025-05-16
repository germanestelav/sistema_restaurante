from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from modules.password_reset.schemas import PasswordResetRequest, PasswordResetConfirm
from modules.password_reset.utils import crear_token_reset, verificar_token_reset, enviar_email_reset
from modules.usuarios.crud import get_usuario_por_username, hash_password
from database.session import get_db
from modules.usuarios.models import Usuario

router = APIRouter(prefix="/password-reset", tags=["password-reset"])

@router.post("/request")
def solicitar_reset(data: PasswordResetRequest, db: Session = Depends(get_db)):
    usuario = get_usuario_por_username(db, data.email)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    token = crear_token_reset(data.email)
    enviar_email_reset(data.email, token)
    return {"msg": "Se ha enviado un enlace de recuperación a tu correo."}

@router.post("/confirm")
def confirmar_reset(data: PasswordResetConfirm, db: Session = Depends(get_db)):
    email = verificar_token_reset(data.token)
    if not email:
        raise HTTPException(status_code=400, detail="Token inválido o expirado")
    usuario = get_usuario_por_username(db, email)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.contrasena = hash_password(data.new_password)
    db.commit()
    return {"msg": "Contraseña actualizada correctamente."}