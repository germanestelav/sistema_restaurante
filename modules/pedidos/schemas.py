from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DetallePedidoBase(BaseModel):
    id_producto: int
    cantidad: int

class DetallePedidoCreate(BaseModel):
    id_producto: int
    cantidad: int

class DetallePedido(DetallePedidoBase):
    id_detalle: int

    class Config:
        orm_mode = True

class PedidoCreate(BaseModel):
    id_mesa: int
    id_estado_pedido: int  # <-- Usar el ID del estado
    detalles: List[DetallePedidoCreate]

class Pedido(BaseModel):
    id_pedido: int
    id_usuario: int
    id_mesa: int
    id_estado_pedido: int
    fecha: datetime
    detalles: List[DetallePedido]

    class Config:
        orm_mode = True

class DetallePedidoUpdate(BaseModel):
    id_detalle: Optional[int]
    id_producto: Optional[int]
    cantidad: Optional[int]

class PedidoUpdate(BaseModel):
    id_estado_pedido: Optional[int]
    id_mesa: Optional[int]
    detalles: Optional[List[DetallePedidoUpdate]]

class PedidoEstadoUpdate(BaseModel):
    id_estado_pedido: int