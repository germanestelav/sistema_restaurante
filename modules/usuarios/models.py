# usuarios/models.py
from sqlalchemy import Column, Integer, String
from database.session import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    apellido = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    contrasena = Column(String(255))
    id_rol = Column(Integer)  # En este caso, es un Integer que puede ser referenciado desde la tabla 'rol'
    estado = Column(String(20), default="activo")  # El estado puede ser 'activo' o 'inactivo'
