from fastapi import Depends, HTTPException, status
from modules.auth.dependencias import get_current_user

def permiso_requerido(roles_permitidos: list[str]):
    def wrapper(user=Depends(get_current_user)):
        if not any(rol in roles_permitidos for rol in user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para acceder a este recurso"
            )
    return Depends(wrapper)