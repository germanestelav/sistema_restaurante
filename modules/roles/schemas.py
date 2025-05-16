from pydantic import BaseModel

class RolBase(BaseModel):
    nombre: str

class RolCreate(RolBase):
    pass

class Rol(RolBase):
    id_rol: int

    class Config:
        orm_mode = True
