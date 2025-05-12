from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configura tu conexión a PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:061270_@localhost/sistema_restaurante"

# Crear el motor de conexión
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crear la sesión para las interacciones con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base para las clases ORM
Base = declarative_base()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
