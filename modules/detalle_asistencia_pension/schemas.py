from pydantic import BaseModel

class DetalleAsistenciaPensionBase(BaseModel):
    id_asistencia: int
    id_producto: int
    cantidad: int = 1

class DetalleAsistenciaPensionCreate(DetalleAsistenciaPensionBase):
    pass

class DetalleAsistenciaPension(DetalleAsistenciaPensionBase):
    id_detalle_asistencia: int

    class Config:
        orm_mode = True