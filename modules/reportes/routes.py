from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from modules.consultas.ventas_por_mozo import obtener_ventas_por_mozo
from modules.reportes.schemas import VentasPorMozo
from database.session import get_db
from modules.permisos.dependencias import permiso_requerido
from modules.consultas.detalles_pedidos_por_mozo import obtener_detalles_pedidos_por_mozo
from modules.reportes.schemas import DetallesPedidosPorMozo


router = APIRouter()

@router.get(
    "/ventas-por-mozo",
    response_model=list[VentasPorMozo],
    dependencies=[permiso_requerido(["Supervisor", "Administrador"])]
)
def ventas_por_mozo(db: Session = Depends(get_db)):
    """
    Devuelve la cantidad de ventas realizadas por cada mozo.
    """
    return obtener_ventas_por_mozo(db)

@router.get(
    "/detalles-pedidos-por-mozo",
    response_model=list[DetallesPedidosPorMozo],
    dependencies=[permiso_requerido(["Supervisor", "Administrador"])]
)
def detalles_pedidos_por_mozo(
    db: Session = Depends(get_db),
    mozo_id: int = None,
    fecha_inicio: str = None,
    fecha_fin: str = None,
    limit: int = 10,
    offset: int = 0,
    limit_pedido: int = 10,
    estado: str = None
):
    return obtener_detalles_pedidos_por_mozo(db, mozo_id, fecha_inicio, fecha_fin, limit, offset, limit_pedido)