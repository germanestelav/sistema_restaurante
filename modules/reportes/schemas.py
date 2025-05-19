from pydantic import BaseModel
from typing import List, Optional

class VentasPorMozo(BaseModel):
    mozo: str
    total_ventas: int
    ventas_efectivo: int
    ventas_yape: int
    ventas_plin: int
    ventas_tarjeta: int
    ventas_transferencia: int
    total_efectivo: float
    total_yape: float
    total_plin: float
    total_tarjeta: float
    total_transferencia: float
    total_ingresos: float


class DetallePedido(BaseModel):
    producto: Optional[str]
    cantidad: Optional[int]
    precio_unitario: Optional[float]

class PedidoMozo(BaseModel):
    id_pedido: int
    fecha: Optional[str]
    estado: Optional[str]
    detalles: List[DetallePedido]
    total: float

class DetallesPedidosPorMozo(BaseModel):
    id_mozo: int
    mozo: str
    pedidos: List[PedidoMozo]