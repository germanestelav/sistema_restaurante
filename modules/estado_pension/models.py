from sqlalchemy import Column, Integer, String
from database.session import Base

class EstadoPension(Base):
    __tablename__ = "estado_pension"

    id_estado_pension = Column(Integer, primary_key=True, autoincrement=True)
    nombre_estado = Column(String(20), unique=True, nullable=False)