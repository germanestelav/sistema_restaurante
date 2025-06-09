from pydantic import BaseModel

class MetodoPagoBase(BaseModel):
    nombre_metodo: str

class MetodoPagoCreate(MetodoPagoBase):
    pass

class MetodoPago(MetodoPagoBase):
    id_metodo_pago: int

    class Config:
        orm_mode = True