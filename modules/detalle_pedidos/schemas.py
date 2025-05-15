from pydantic import BaseModel

class DetallePedidoBase(BaseModel):
    id_producto: int
    cantidad: int
    precio_unitario: float

class DetallePedidoCreate(DetallePedidoBase):
    pass  # Se usa para crear un detalle de pedido

class DetallePedido(DetallePedidoBase):
    id_detalle: int

    class Config:
        orm_mode = True  # Permite convertir el modelo SQLAlchemy a diccionario
