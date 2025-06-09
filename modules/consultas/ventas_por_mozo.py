from sqlalchemy.orm import Session
from sqlalchemy import func, case
from modules.usuarios.models import Usuario
from modules.pedidos.models import Pedido
from modules.pagos.models import Pago
from datetime import datetime
from utils.logger import get_logger

logger = get_logger("modules.consultas.ventas_por_mozo")

def obtener_ventas_por_mozo(
    db: Session,
    mozo_id: int = None,
    fecha_inicio: str = None,
    fecha_fin: str = None,
    estado: str = None
):
    logger.info("Iniciando consulta de ventas por mozo")
    query = db.query(
        Usuario.nombre.label("mozo"),
        func.count(Pedido.id_pedido).label("total_ventas"),
        func.sum(case((Pago.metodo_pago == "efectivo", 1), else_=0)).label("ventas_efectivo"),
        func.sum(case((Pago.metodo_pago == "yape", 1), else_=0)).label("ventas_yape"),
        func.sum(case((Pago.metodo_pago == "plin", 1), else_=0)).label("ventas_plin"),
        func.sum(case((Pago.metodo_pago == "tarjeta", 1), else_=0)).label("ventas_tarjeta"),
        func.sum(case((Pago.metodo_pago == "transferencia", 1), else_=0)).label("ventas_transferencia"),
        func.sum(case((Pago.metodo_pago == "efectivo", Pago.monto_total), else_=0)).label("total_efectivo"),
        func.sum(case((Pago.metodo_pago == "yape", Pago.monto_total), else_=0)).label("total_yape"),
        func.sum(case((Pago.metodo_pago == "plin", Pago.monto_total), else_=0)).label("total_plin"),
        func.sum(case((Pago.metodo_pago == "tarjeta", Pago.monto_total), else_=0)).label("total_tarjeta"),
        func.sum(case((Pago.metodo_pago == "transferencia", Pago.monto_total), else_=0)).label("total_transferencia"),
    ).join(Pedido, Pedido.id_usuario == Usuario.id_usuario
    ).join(Pago, Pago.id_pedido == Pedido.id_pedido)

    if mozo_id:
        logger.info(f"Filtrando por mozo_id: {mozo_id}")
        query = query.filter(Usuario.id_usuario == mozo_id)
    if fecha_inicio:
        logger.info(f"Aplicando filtro desde fecha_inicio: {fecha_inicio}")
        fecha_inicio = datetime.fromisoformat(fecha_inicio)
        query = query.filter(Pedido.fecha >= fecha_inicio)
    if fecha_fin:
        logger.info(f"Aplicando filtro hasta fecha_fin: {fecha_fin}")
        fecha_fin = datetime.fromisoformat(fecha_fin)
        query = query.filter(Pedido.fecha <= fecha_fin)
    if estado:
        logger.info(f"Filtrando por estado del pedido: {estado}")
        query = query.filter(Pedido.estado == estado)

    resultados = query.group_by(Usuario.id_usuario).all()
    logger.info(f"Se encontraron {len(resultados)} resultados de ventas por mozo")

    return [
        {
            "mozo": r.mozo,
            "total_ventas": r.total_ventas,
            "ventas_efectivo": r.ventas_efectivo,
            "ventas_yape": r.ventas_yape,
            "ventas_plin": r.ventas_plin,
            "ventas_tarjeta": r.ventas_tarjeta,
            "ventas_transferencia": r.ventas_transferencia,
            "total_efectivo": float(r.total_efectivo or 0),
            "total_yape": float(r.total_yape or 0),
            "total_plin": float(r.total_plin or 0),
            "total_tarjeta": float(r.total_tarjeta or 0),
            "total_transferencia": float(r.total_transferencia or 0),
            "total_ingresos": float(
                (r.total_efectivo or 0) +
                (r.total_yape or 0) +
                (r.total_plin or 0) +
                (r.total_tarjeta or 0) +
                (r.total_transferencia or 0)
            ),
        }
        for r in resultados
    ]