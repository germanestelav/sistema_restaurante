from sqlalchemy.orm import Session
from sqlalchemy import func
from modules.usuarios.models import Usuario
from modules.pedidos.models import Pedido  # Ajusta el import si tu modelo está en otro lugar

def obtener_ventas_por_mozo(db: Session):
    """
    Devuelve una lista con el nombre del mozo y la cantidad de ventas (pedidos) que realizó.
    """
    resultados = (
        db.query(
            Usuario.nombre.label("mozo"),
            func.count(Pedido.id_pedido).label("cantidad_ventas")
        )
        .join(Pedido, Pedido.id_usuario == Usuario.id_usuario)
        .group_by(Usuario.id_usuario)
        .all()
    )
    # Opcional: convertir a lista de diccionarios
    return [{"mozo": r.mozo, "cantidad_ventas": r.cantidad_ventas} for r in resultados]