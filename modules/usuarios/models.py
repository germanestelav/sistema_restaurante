from sqlalchemy import Column, Integer, String, Text
from database.session import Base
from sqlalchemy.orm import relationship
from modules.roles.models import Rol

class Usuario(Base):
    __tablename__ = 'usuarios'

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False, unique=True)
    contrasena = Column(Text, nullable=False)  # Contraseña cifrada
    estado = Column(String(20), default='activo')
    numero_identificacion = Column(String(50), unique=True, nullable=False)

# Relación con Pedido
    pedidos = relationship("Pedido", back_populates="usuario")  # Relación con Pedido
    roles_asignados = relationship("UsuarioRol", back_populates="usuario", cascade="all, delete-orphan")