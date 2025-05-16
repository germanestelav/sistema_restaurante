# productos/models.py
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from database.session import Base

class Producto(Base):
    __tablename__ = 'productos'

    id_producto = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    precio = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, default=0)
    estado = Column(String(20), default="activo")  # campo estado
    id_categoria = Column(Integer, ForeignKey('categorias.id_categoria'))

    categoria_rel = relationship("Categoria", back_populates="productos")
    detalles = relationship("DetallePedido", back_populates="producto")
