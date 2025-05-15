from pydantic import BaseModel

class MesaBase(BaseModel):
    numero: int
    capacidad: int
    estado: str = "libre"  # El estado por defecto es "libre"

class MesaCreate(MesaBase):
    pass  # Esquema para crear una mesa

class Mesa(MesaBase):
    id_mesa: int  # ID de la mesa, solo para la respuesta

    class Config:
        orm_mode = True  # Permite convertir el modelo SQLAlchemy a un diccionario
