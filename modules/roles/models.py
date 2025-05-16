from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.session import Base

class Rol(Base):
    __tablename__ = "roles"

    id_rol = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

    # Relación con la tabla intermedia UsuarioRol
    usuarios_asignados = relationship("UsuarioRol", back_populates="rol", cascade="all, delete-orphan")
