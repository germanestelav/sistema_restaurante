# productos/schemas.py
from pydantic import BaseModel

class ProductoBase(BaseModel):
    nombre: str
    descripcion: str = None
    precio: float
    categoria: str = None
    stock: int = 0

class ProductoCreate(ProductoBase):
    pass  # Para la creación de productos

class Producto(ProductoBase):
    id_producto: int

    class Config:
        orm_mode = True  # Permite convertir el modelo SQLAlchemy a diccionario
