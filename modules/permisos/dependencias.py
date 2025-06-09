from fastapi import Depends, HTTPException, status
from modules.auth.dependencias import get_current_user
from utils.logger import get_logger

logger = get_logger("modules.permisos.dependencias")

def permiso_requerido(roles_permitidos: list[str]):
    def wrapper(user=Depends(get_current_user)):
        if not any(rol in roles_permitidos for rol in user.roles):
            logger.warning(f"Acceso denegado para usuario '{getattr(user, 'username', 'desconocido')}'. Roles requeridos: {roles_permitidos}. Roles del usuario: {user.roles}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para acceder a este recurso"
            )
        logger.info(f"Acceso concedido para usuario '{getattr(user, 'username', 'desconocido')}' con roles: {user.roles}")
    return Depends(wrapper)