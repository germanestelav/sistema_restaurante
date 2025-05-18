from pydantic import BaseModel

class VentasPorMozo(BaseModel):
    mozo: str
    cantidad_ventas: int