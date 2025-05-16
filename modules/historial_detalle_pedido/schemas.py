from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional

class HistorialDetallePedidoBase(BaseModel):
    id_detalle_original: Optional[int]
    id_producto_anterior: Optional[int]
    cantidad_anterior: int
    precio_unitario_anterior: Decimal
    motivo: Optional[str]

class HistorialDetallePedidoCreate(HistorialDetallePedidoBase):
    pass

class HistorialDetallePedido(HistorialDetallePedidoBase):
    id_historial: int
    fecha_modificacion: datetime

    class Config:
        orm_mode = True
