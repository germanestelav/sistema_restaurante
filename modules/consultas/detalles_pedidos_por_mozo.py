from sqlalchemy.orm import Session, joinedload
from modules.usuarios.models import Usuario
from modules.pedidos.models import Pedido
from modules.detalle_pedidos.models import DetallePedido
from datetime import datetime
from modules.roles.models import Rol
from utils.logger import get_logger

logger = get_logger("modules.consultas.detalles_pedidos_por_mozo")

def obtener_detalles_pedidos_por_mozo(
    db: Session,
    mozo_id: int = None,
    fecha_inicio: str = None,
    fecha_fin: str = None,
    limit: int = 10,
    offset: int = 0,
    limit_pedido: int = 10,
    estado: str = None
):
    logger.info("Iniciando consulta de pedidos por mozo")

    # Convertir fechas si vienen como string
    if fecha_inicio:
        logger.info(f"Fecha inicio recibida: {fecha_inicio}")
        fecha_inicio = datetime.fromisoformat(fecha_inicio)
    if fecha_fin:
        logger.info(f"Fecha fin recibida: {fecha_fin}")
        fecha_fin = datetime.fromisoformat(fecha_fin)

    # Realizar la consulta
    query = db.query(Usuario).join(Usuario.roles_asignados).join(Rol).filter(Rol.nombre == "Mozo").options(
        joinedload(Usuario.pedidos)
        .joinedload(Pedido.detalles)
        .joinedload(DetallePedido.producto)
    )
    if mozo_id:
        logger.info(f"Filtrando por mozo_id: {mozo_id}")
        query = query.filter(Usuario.id_usuario == mozo_id)
    # Aquí aplicas paginación
    mozos = query.offset(offset).limit(limit).all()
    logger.info(f"Se encontraron {len(mozos)} mozos")
    resultado = []

    for mozo in mozos:
        logger.info(f"Procesando mozo: {mozo.nombre} (ID: {mozo.id_usuario})")
        pedidos = []
        for pedido in mozo.pedidos[:limit_pedido]:
            if fecha_inicio and pedido.fecha < fecha_inicio:
                continue
            if fecha_fin and pedido.fecha > fecha_fin:
                continue
            if estado and pedido.estado != estado:
                continue
            detalles = [
                {
                    "producto": detalle.producto.nombre if getattr(detalle, "producto", None) is not None else None,
                    "cantidad": detalle.cantidad,
                    "precio_unitario": detalle.precio_unitario
                }
                for detalle in getattr(pedido, "detalles", [])
            ]
            total = sum((d["cantidad"] or 0) * (d["precio_unitario"] or 0) for d in detalles)
            pedidos.append({
                "id_pedido": pedido.id_pedido,
                "fecha": str(pedido.fecha) if getattr(pedido, "fecha", None) is not None else None,
                "estado": str(pedido.estado) if getattr(pedido, "estado", None) is not None else None,
                "detalles": detalles,
                "total": total
            })
        resultado.append({
            "id_mozo": mozo.id_usuario,
            "mozo": mozo.nombre,
            "pedidos": pedidos
        })
        logger.info(f"Mozo {mozo.nombre} tiene {len(pedidos)} pedidos procesados")
    
    logger.info("Consulta de pedidos por mozo finalizada")
    return resultado