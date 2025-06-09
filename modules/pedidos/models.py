from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from database.session import Base
from modules.usuarios.models import Usuario
from modules.pagos.models import Pago
from modules.detalle_pedidos.models import DetallePedido

class Pedido(Base):
    __tablename__ = 'pedidos'

    id_pedido = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)  # Relación con Usuario
    id_mesa = Column(Integer, ForeignKey('mesas.id_mesa'), nullable=False)  # Relación con Mesa
    id_estado_pedido = Column(Integer, ForeignKey("estados_pedidos.id_estado_pedido"))  # Relación con EstadoPedido
    fecha = Column(TIMESTAMP, default=datetime.utcnow)  # Fecha del pedido

    # Relaciones a nivel de Pedido
    usuario = relationship("Usuario")
    mesa = relationship("Mesa")
    detalles = relationship("DetallePedido", back_populates="pedido")
    pagos = relationship("Pago", back_populates="pedido")
    estado = relationship("EstadoPedido", back_populates="pedidos")
