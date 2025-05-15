from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database.session import Base

class Mesa(Base):
    __tablename__ = 'mesas'

    id_mesa = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(Integer, nullable=False, unique=True)  # El número de la mesa
    capacidad = Column(Integer, nullable=False)  # Capacidad de la mesa (número de personas que puede atender)
    estado = Column(String(20), default="libre")  # Estado de la mesa (libre, ocupada, reservada)

# Relación con Pedido
    pedidos = relationship("Pedido", back_populates="mesa")  # Relación con Pedido
