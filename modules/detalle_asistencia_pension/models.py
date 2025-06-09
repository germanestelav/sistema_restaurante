from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.session import Base

class DetalleAsistenciaPension(Base):
    __tablename__ = "detalle_asistencia_pension"

    id_detalle_asistencia = Column(Integer, primary_key=True, autoincrement=True)
    id_asistencia = Column(Integer, ForeignKey("asistencias_pension.id_asistencia"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    cantidad = Column(Integer, nullable=False, default=1)

    asistencia = relationship("AsistenciaPension", back_populates="detalles")
    producto = relationship("Producto")