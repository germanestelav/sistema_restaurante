from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas

# Crear una nueva mesa
def create_mesa(db: Session, mesa: schemas.MesaCreate):
    db_mesa = models.Mesa(
        numero=mesa.numero,
        capacidad=mesa.capacidad,
        estado=mesa.estado
    )
    db.add(db_mesa)
    db.commit()
    db.refresh(db_mesa)
    return db_mesa

# Obtener todas las mesas
def get_mesas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Mesa).offset(skip).limit(limit).all()

# Obtener una mesa por ID
def get_mesa(db: Session, mesa_id: int):
    return db.query(models.Mesa).filter(models.Mesa.id_mesa == mesa_id).first()

# Actualizar una mesa
def update_mesa(db: Session, mesa_id: int, mesa: schemas.MesaCreate):
    db_mesa = db.query(models.Mesa).filter(models.Mesa.id_mesa == mesa_id).first()
    if not db_mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    db_mesa.numero = mesa.numero
    db_mesa.capacidad = mesa.capacidad
    db_mesa.estado = mesa.estado
    db.commit()
    db.refresh(db_mesa)
    return db_mesa

# Eliminar una mesa
def delete_mesa(db: Session, mesa_id: int):
    db_mesa = db.query(models.Mesa).filter(models.Mesa.id_mesa == mesa_id).first()
    if not db_mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    db.delete(db_mesa)
    db.commit()
    return db_mesa
