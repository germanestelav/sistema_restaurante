from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class ClientePensionBase(BaseModel):
    nombre: str
    apellido: str
    dni: str
    telefono: str | None = None
    fecha_inicio: date
    fecha_fin: date
    tipo_pension: str
    tipo_pago: str
    pago_adelantado: Decimal = 0
    id_estado_pension: int
    observacion: str | None = None

class ClientePensionCreate(ClientePensionBase):
    pass

class ClientePension(ClientePensionBase):
    id_cliente_pension: int

    class Config:
        orm_mode = True