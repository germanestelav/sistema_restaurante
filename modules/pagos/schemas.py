from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class PagoBase(BaseModel):
    id_pedido: int
    monto_total: Decimal
    metodo_pago: str

class PagoCreate(PagoBase):
    pass

class Pago(PagoBase):
    id_pago: int
    fecha_pago: datetime

    class Config:
        orm_mode = True
