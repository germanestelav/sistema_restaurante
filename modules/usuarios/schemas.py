# usuarios/schemas.py
from pydantic import BaseModel
from typing import Optional

class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    email: str
    contrasena: str
    id_rol: int
    estado: Optional[str] = "activo"  # "activo" por defecto

class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id_usuario: int

    class Config:
        orm_mode = True  # Esto permite que SQLAlchemy sea utilizado con Pydantic
