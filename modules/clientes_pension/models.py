from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from database.session import Base

class ClientePension(Base):
    __tablename__ = "clientes_pension"

    id_cliente_pension = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    dni = Column(String(20), unique=True, nullable=False)
    telefono = Column(String(12))
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    tipo_pension = Column(String(50), nullable=False)
    tipo_pago = Column(String(20), nullable=False)
    pago_adelantado = Column(Numeric(10, 2), default=0)
    id_estado_pension = Column(Integer, ForeignKey("estado_pension.id_estado_pension"), nullable=False)
    observacion = Column(String(200))

    estado = relationship("EstadoPension")
    pagos = relationship("PagoPension", back_populates="cliente")