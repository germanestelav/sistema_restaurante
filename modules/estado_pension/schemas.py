from pydantic import BaseModel

class EstadoPensionBase(BaseModel):
    nombre_estado: str

class EstadoPensionCreate(EstadoPensionBase):
    pass

class EstadoPension(EstadoPensionBase):
    id_estado_pension: int

    class Config:
        orm_mode = True