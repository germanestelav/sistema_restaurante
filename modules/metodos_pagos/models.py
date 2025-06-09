from sqlalchemy import Column, Integer, String
from database.session import Base

class MetodoPago(Base):
    __tablename__ = "metodos_pagos"
    id_metodo_pago = Column(Integer, primary_key=True, index=True)
    nombre_metodo = Column(String(50), unique=True, nullable=False)