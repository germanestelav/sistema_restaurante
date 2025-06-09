# modules/historial_detalle_pedidos/models.py
from sqlalchemy import Column, Integer, ForeignKey, Numeric, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from database.session import Base

class HistorialDetallePedido(Base):
    __tablename__ = "historial_detalle_pedido"

    id_historial = Column(Integer, primary_key=True, autoincrement=True)
    id_detalle_original = Column(Integer, ForeignKey("detalle_pedidos.id_detalle"), nullable=True)
    id_producto_anterior = Column(Integer, ForeignKey("productos.id_producto"), nullable=True)
    cantidad_anterior = Column(Integer, nullable=False)
    precio_unitario_anterior = Column(Numeric, nullable=False)
    fecha_modificacion = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    motivo = Column(Text, nullable=True)

    detalle_pedido = relationship("DetallePedido", back_populates="historiales")
    producto_anterior = relationship("Producto")

    def __repr__(self):
        return f"<HistorialDetallePedido id={self.id_historial} detalle={self.detalle_pedido}>"