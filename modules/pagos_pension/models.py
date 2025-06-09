from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.session import Base

class PagoPension(Base):
    __tablename__ = "pagos_pension"

    id_pago_pension = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente_pension = Column(Integer, ForeignKey("clientes_pension.id_cliente_pension"), nullable=False)
    fecha_pago = Column(DateTime, nullable=False)
    monto = Column(Numeric(10, 2), nullable=False)
    periodo = Column(String(50))
    id_metodo_pago = Column(Integer, ForeignKey("metodos_pagos.id_metodo_pago"), nullable=False)
    observacion = Column(String(200))

    cliente = relationship("ClientePension", back_populates="pagos")
    metodo_pago = relationship("MetodoPago")