from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DetallePedido(BaseModel):
    id_detalle: int
    id_producto: int
    cantidad: int
    precio_unitario: float

    class Config:
        orm_mode = True

class PedidoCreate(BaseModel):
    id_usuario: int
    id_mesa: int
    estado: Optional[str] = 'pendiente'
    detalles: List[DetallePedido]

class Pedido(BaseModel):
    id_pedido: int
    id_usuario: int
    id_mesa: int
    estado: Optional[str]
    fecha: datetime
    detalles: List[DetallePedido]

    class Config:
        orm_mode = True
