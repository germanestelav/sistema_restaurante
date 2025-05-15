from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from database.session import Base



class DetallePedido(Base):
    __tablename__ = 'detalle_pedidos'

    id_detalle = Column(Integer, primary_key=True, autoincrement=True)
    id_pedido = Column(Integer, ForeignKey('pedidos.id_pedido'), nullable=False)  # Relación con Pedido
    id_producto = Column(Integer, ForeignKey('productos.id_producto'), nullable=False)  # Relación con Producto
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(DECIMAL(10, 2), nullable=False)

    # Relaciones
    pedido = relationship("Pedido", back_populates="detalles")
    producto = relationship("Producto")  # Relación hacia Producto