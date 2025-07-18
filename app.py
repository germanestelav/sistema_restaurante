from fastapi import FastAPI
from utils.logger import get_logger

# Importar todos los modelos para que SQLAlchemy los registre y evite errores de relaciones
import modules.productos.models
import modules.pedidos.models
import modules.detalle_pedidos.models
import modules.usuarios.models
import modules.mesas.models
import modules.pagos.models
import modules.roles.models
import modules.categorias.models
import modules.usuarios_roles.models
import modules.historial_detalle_pedido.models

from modules.usuarios.routes import router as usuarios_router
from modules.productos.routes import router as productos_router
from modules.pedidos.routes import router as pedidos_router
from modules.detalle_pedidos.routes import router as detalle_pedidos_router
from modules.mesas.routes import router as mesas_router
from modules.pagos.routes import router as pagos_router
from modules.roles.routes import router as roles_router
from modules.categorias.routes import router as categorias_router
from modules.usuarios_roles.routes import router as usuario_rol_router
from modules.historial_detalle_pedido.routes import router as historial_detalle_pedido_router
from modules.auth.routes import router as auth_router
from modules.password_reset.routes import router as password_reset_router
from modules.reportes.routes import router as reportes_router
from modules.metodos_pagos.routes import router as metodos_pagos_router
from modules.estados_pedidos.routes import router as estados_pedidos_router
from modules.pagos_pension.routes import router as pagos_pension_router
from modules.clientes_pension.routes import router as clientes_pension_router
from modules.estado_pension.routes import router as estado_pension_router
from modules.asistencias_pension.routes import router as asistencias_pension_router
from modules.detalle_asistencia_pension.routes import router as detalle_asistencia_pension_router

app = FastAPI()
logger = get_logger("app")

logger.info("Aplicación FastAPI iniciada")

app.include_router(auth_router)
app.include_router(password_reset_router)
app.include_router(usuarios_router, prefix="/usuarios", tags=["usuarios"])
app.include_router(productos_router, prefix="/productos", tags=["productos"])
app.include_router(pedidos_router, prefix="/pedidos", tags=["pedidos"])
app.include_router(detalle_pedidos_router, prefix="/detalle_pedidos", tags=["detalle_pedidos"])
app.include_router(mesas_router, prefix="/mesas", tags=["mesas"])
app.include_router(pagos_router, prefix="/pagos", tags=["pagos"])
app.include_router(roles_router, prefix="/roles", tags=["roles"])
app.include_router(categorias_router, prefix="/categorias", tags=["categorias"])
app.include_router(usuario_rol_router, prefix="/usuario_rol", tags=["usuario_rol"])
app.include_router(historial_detalle_pedido_router, prefix="/historial_detalle_pedido", tags=["historial_detalle_pedido"])
app.include_router(reportes_router, prefix="/reportes", tags=["reportes"])
app.include_router(metodos_pagos_router, prefix="/metodos_pagos", tags=["metodos_pagos"])
app.include_router(estados_pedidos_router, prefix="/estados_pedidos", tags=["estados_pedidos"])
app.include_router(pagos_pension_router, prefix="/pagos_pension", tags=["Pagos Pensión"])
app.include_router(clientes_pension_router, prefix="/clientes_pension", tags=["Clientes Pensión"])
app.include_router(estado_pension_router, prefix="/estado_pension", tags=["Estado Pensión"])
app.include_router(asistencias_pension_router, prefix="/asistencias_pension", tags=["Asistencias Pensión"])
app.include_router(detalle_asistencia_pension_router, prefix="/detalle_asistencia_pension", tags=["Detalle Asistencia Pensión"])