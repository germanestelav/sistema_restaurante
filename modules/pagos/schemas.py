from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class PagoCreate(BaseModel):
    id_pedido: int
    id_metodo_pago: int
    # monto_total eliminado

class Pago(BaseModel):
    id_pago: int
    id_pedido: int
    id_metodo_pago: int
    monto_total: Decimal
    fecha_pago: datetime

    class Config:
        orm_mode = True
