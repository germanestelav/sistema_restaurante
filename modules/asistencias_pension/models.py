from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from database.session import Base

class AsistenciaPension(Base):
    __tablename__ = "asistencias_pension"

    id_asistencia = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente_pension = Column(Integer, ForeignKey("clientes_pension.id_cliente_pension"), nullable=False)
    fecha = Column(DateTime, nullable=False)
    observacion = Column(String(200))

    cliente = relationship("ClientePension")
    detalles = relationship("DetalleAsistenciaPension", back_populates="asistencia")