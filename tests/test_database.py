# Mostrar tablas y datos de una base de datos PostgreSQL
# Este script se conecta a una base de datos PostgreSQL y muestra las tablas y sus datos.

from sqlalchemy import create_engine, inspect, MetaData, Table
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:061270_@localhost/sistema_restaurante"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def mostrar_tablas_y_datos():
    inspector = inspect(engine)
    metadata = MetaData()
    metadata.reflect(bind=engine)

    session = SessionLocal()

    print("Tablas y datos (limit 5 filas por tabla):\n")

    for table_name in inspector.get_table_names():
        print(f"Tabla: {table_name}")

        fks = inspector.get_foreign_keys(table_name)
        if fks:
            print(" Relaciones FK:")
            for fk in fks:
                print(f"  - Columna(s) {fk['constrained_columns']} -> Tabla referenciada: {fk['referred_table']}")

        table = Table(table_name, metadata, autoload_with=engine)
        query = session.query(table).limit(5)
        resultados = query.all()

        if resultados:
            for row in resultados:
                # Conversión segura para imprimir
                print(" ", dict(row._mapping))
        else:
            print("  No hay datos.")

        print("\n" + "-"*40 + "\n")

    session.close()

if __name__ == "__main__":
    mostrar_tablas_y_datos()
