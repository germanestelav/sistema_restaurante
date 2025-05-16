from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.session import Base

class UsuarioRol(Base):
    __tablename__ = "usuario_rol"

    id_usuario_rol = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_rol = Column(Integer, ForeignKey("roles.id_rol"), nullable=False)

    # Relación con Usuario
    usuario = relationship("Usuario", back_populates="roles_asignados")
    
    # Relación con Rol
    rol = relationship("Rol", back_populates="usuarios_asignados")
