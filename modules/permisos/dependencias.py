from fastapi import Depends, HTTPException, status
from modules.auth.dependencias import get_current_user

def supervisor_o_admin(user = Depends(get_current_user)):
    # user.roles debe ser una lista de roles
    if not any(rol in ["supervisor", "administrador"] for rol in getattr(user, "roles", [])):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para realizar esta acción"
        )
    return user