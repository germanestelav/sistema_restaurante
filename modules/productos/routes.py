# productos/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from database.session import get_db  # Función que conecta a la base de datos
from utils.logger import get_logger

router = APIRouter()
logger = get_logger("productos.routes")

# Ruta para crear un producto
@router.post("/", response_model=schemas.Producto)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para crear producto: {producto}")
    return crud.create_producto(db=db, producto=producto)

# Ruta para obtener todos los productos
@router.get("/", response_model=list[schemas.Producto])
def leer_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para listar productos (skip={skip}, limit={limit})")
    return crud.get_productos(db=db, skip=skip, limit=limit)


@router.get("/con-stock", response_model=list[schemas.Producto])
def leer_productos_con_stock(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para listar productos con stock (skip={skip}, limit={limit})")
    return crud.get_productos_con_stock(db=db, skip=skip, limit=limit)


# Ruta para obtener un producto por ID
@router.get("/{producto_id}", response_model=schemas.Producto)
def leer_producto(producto_id: int, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para obtener producto ID: {producto_id}")
    db_producto = crud.get_producto(db=db, producto_id=producto_id)
    if db_producto is None:
        logger.warning(f"Producto no encontrado con ID: {producto_id}")
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

# Ruta para actualizar un producto
@router.put("/{producto_id}", response_model=schemas.Producto)
def actualizar_producto(producto_id: int, producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para actualizar producto ID: {producto_id} con datos: {producto}")
    db_producto = crud.update_producto(db=db, producto_id=producto_id, producto=producto)
    if db_producto is None:
        logger.warning(f"No se pudo actualizar. Producto no encontrado con ID: {producto_id}")
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

# Ruta para eliminar un producto
@router.delete("/{producto_id}", response_model=schemas.Producto)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para eliminar producto ID: {producto_id}")
    db_producto = crud.delete_producto(db=db, producto_id=producto_id)
    if db_producto is None:
        logger.warning(f"No se pudo eliminar. Producto no encontrado con ID: {producto_id}")
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto
