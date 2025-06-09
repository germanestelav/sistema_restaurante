from sqlalchemy import Column, Integer, String
from database.session import Base
from sqlalchemy.orm import relationship

class EstadoPedido(Base):
    __tablename__ = "estados_pedidos"
    id_estado_pedido = Column(Integer, primary_key=True, index=True)
    nombre_estado = Column(String(50), unique=True, nullable=False)

    # Definición de la relación con la tabla Pedido
    pedidos = relationship("Pedido", back_populates="estado")