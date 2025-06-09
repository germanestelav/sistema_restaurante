from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from database.session import get_db
from utils.logger import get_logger

logger = get_logger("categorias.router")

router = APIRouter()

@router.post("/", response_model=schemas.Categoria)
def create_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud POST para crear categoría: {categoria}")
    return crud.create_categoria(db=db, categoria=categoria)

@router.get("/", response_model=list[schemas.Categoria])
def read_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Solicitud GET para obtener categorías con skip={skip}, limit={limit}")
    categorias = crud.get_categorias(db=db, skip=skip, limit=limit)
    logger.info(f"Se encontraron {len(categorias)} categorías")
    return categorias

@router.get("/{id_categoria}", response_model=schemas.Categoria)
def read_categoria(id_categoria: int, db: Session = Depends(get_db)):
    logger.info(f"Solicitud GET para obtener categoría ID {id_categoria}")
    db_categoria = crud.get_categoria(db=db, id_categoria=id_categoria)
    if not db_categoria:
        logger.warning(f"Categoría ID {id_categoria} no encontrada")
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    logger.info(f"Categoría encontrada: {db_categoria}")
    return db_categoria

@router.put("/{id_categoria}", response_model=schemas.Categoria)
def update_categoria(id_categoria: int, categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud PUT para actualizar categoría ID {id_categoria} con datos: {categoria}")
    return crud.update_categoria(db=db, id_categoria=id_categoria, categoria=categoria)

@router.delete("/{id_categoria}", response_model=schemas.Categoria)
def delete_categoria(id_categoria: int, db: Session = Depends(get_db)):
    logger.info(f"Solicitud DELETE para eliminar categoría ID {id_categoria}")
    return crud.delete_categoria(db=db, id_categoria=id_categoria)
