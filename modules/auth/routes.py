from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from modules.auth.jwt_utils import crear_token
from modules.auth.schemas import Token
from modules.usuarios.crud import get_usuario_por_username, verify_password
from database.session import get_db  # Ajusta el import según tu proyecto
from modules.auth.dependencias import get_current_user
from utils.logger import get_logger

logger = get_logger("modules.auth.routes")

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario_db = get_usuario_por_username(db, form_data.username)
    if not usuario_db or not verify_password(form_data.password, usuario_db.contrasena):
        logger.warning(f"Intento de login fallido para username: {form_data.username}")
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    
    # Obtener todos los roles asignados
    roles = [relacion.rol.nombre for relacion in usuario_db.roles_asignados]
    if not roles:
        logger.warning(f"Usuario {form_data.username} no tiene roles asignados")
        raise HTTPException(status_code=400, detail="El usuario no tiene rol asignado")
    token = crear_token({"sub": usuario_db.correo, "roles": roles})
    logger.info(f"Usuario {form_data.username} autenticado exitosamente. Token generado.")
    return {"access_token": token, "token_type": "bearer"}

@router.get("/mis-roles")
def mis_roles(user = Depends(get_current_user)):
    logger.info(f"Usuario {getattr(user, 'username', 'desconocido')} consultó sus roles")
    return {"roles": getattr(user, "roles", [])}