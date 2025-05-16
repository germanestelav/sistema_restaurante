# productos/schemas.py
from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: Decimal
    stock: int
    estado: Optional[str] = "activo"
    id_categoria: int

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id_producto: int

    class Config:
        orm_mode = True
