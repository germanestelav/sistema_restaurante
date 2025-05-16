from pydantic import BaseModel

class UsuarioRolBase(BaseModel):
    id_usuario: int
    id_rol: int

class UsuarioRolCreate(UsuarioRolBase):
    pass

class UsuarioRol(UsuarioRolBase):
    id_usuario_rol: int

    class Config:
        orm_mode = True

class UsuarioRolUpdate(BaseModel):
    id_usuario: int
    id_rol: int

    class Config:
        orm_mode = True