# productos/models.py
from sqlalchemy import Column, Integer, String, Text, DECIMAL
from database.session import Base
class Producto(Base):
    __tablename__ = 'productos'

    id_producto = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    precio = Column(DECIMAL(10, 2), nullable=False)
    categoria = Column(String(50))
    stock = Column(Integer, default=0)
