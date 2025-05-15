# database/session.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de la base de datos PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:061270_@localhost/sistema_restaurante"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()  # Creamos una nueva sesión
    try:
        yield db  # Retornamos la sesión
    finally:
        db.close()  # Cerramos la sesión después de usarla
