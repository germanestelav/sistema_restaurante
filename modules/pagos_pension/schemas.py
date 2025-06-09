from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class PagoPensionBase(BaseModel):
    id_cliente_pension: int
    fecha_pago: datetime
    monto: Decimal
    periodo: str | None = None
    id_metodo_pago: int
    observacion: str | None = None

class PagoPensionCreate(PagoPensionBase):
    pass

class PagoPension(PagoPensionBase):
    id_pago_pension: int

    class Config:
        orm_mode = True