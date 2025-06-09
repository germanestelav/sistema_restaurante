from pydantic import BaseModel
from datetime import datetime

class AsistenciaPensionBase(BaseModel):
    id_cliente_pension: int
    fecha: datetime
    observacion: str | None = None

class AsistenciaPensionCreate(AsistenciaPensionBase):
    pass

class AsistenciaPension(AsistenciaPensionBase):
    id_asistencia: int

    class Config:
        orm_mode = True