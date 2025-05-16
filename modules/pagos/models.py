from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from database.session import Base

class Pago(Base):
    __tablename__ = "pagos"

    id_pago = Column(Integer, primary_key=True, autoincrement=True)
    id_pedido = Column(Integer, ForeignKey("pedidos.id_pedido"), nullable=False)
    monto_total = Column(Numeric, nullable=False)
    fecha_pago = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    metodo_pago = Column(String(50), nullable=False)

    pedido = relationship("Pedido")
