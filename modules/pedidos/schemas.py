from pydantic import BaseModel
from typing import List, Optional

# Esquema para Producto en detalle del pedido
class DetallePedido(BaseModel):
    id_producto: int
    cantidad: int
    precio_unitario: float

# Esquema para la creación de un pedido
class PedidoCreate(BaseModel):
    id_usuario: int
    id_mesa: int
    estado: Optional[str] = 'pendiente'
    detalles: List[DetallePedido]  # Relación con los productos que tiene el pedido

# Esquema para devolver los detalles de un pedido
class Pedido(PedidoCreate):
    id_pedido: int
    fecha: str  # Fecha de creación del pedido

    class Config:
        orm_mode = True  # Permite convertir el modelo SQLAlchemy a un diccionario
