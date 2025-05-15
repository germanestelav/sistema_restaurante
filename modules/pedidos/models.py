from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from database.session import Base
from modules.usuarios.models import Usuario


class Pedido(Base):
    __tablename__ = 'pedidos'

    id_pedido = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)  # Relación con Usuario
    id_mesa = Column(Integer, ForeignKey('mesas.id_mesa'), nullable=False)  # Relación con Mesa
    estado = Column(String(20), default="pendiente")  # Estado del pedido (pendiente, en_proceso, entregado, cancelado)
    fecha = Column(TIMESTAMP, default=datetime.utcnow)  # Fecha del pedido

    # Relaciones a nivel de Pedido
    usuario = relationship("Usuario")  # Relación con Usuario
    mesa = relationship("Mesa")  # Relación con Mesa
    detalles = relationship("DetallePedido", back_populates="pedido")  # Detalles de los productos del pedido
