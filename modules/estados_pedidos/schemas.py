from pydantic import BaseModel

class EstadoPedidoBase(BaseModel):
    nombre_estado: str

class EstadoPedidoCreate(EstadoPedidoBase):
    pass

class EstadoPedido(EstadoPedidoBase):
    id_estado_pedido: int

    class Config:
        orm_mode = True