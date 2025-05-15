from fastapi import FastAPI

# Importar todos los modelos para que SQLAlchemy los registre y evite errores de relaciones
import modules.productos.models
import modules.pedidos.models
import modules.detalle_pedidos.models
import modules.usuarios.models
import modules.mesas.models

# Importar routers
from modules.usuarios.routes import router as usuarios_router
from modules.productos.routes import router as productos_router
from modules.pedidos.routes import router as pedidos_router
from modules.detalle_pedidos.routes import router as detalle_pedidos_router
from modules.mesas.routes import router as mesas_router

app = FastAPI()

# Incluir las rutas con prefijos y tags adecuados
app.include_router(usuarios_router, prefix="/usuarios", tags=["usuarios"])
app.include_router(productos_router, prefix="/productos", tags=["productos"])
app.include_router(pedidos_router, prefix="/pedidos", tags=["pedidos"])
app.include_router(detalle_pedidos_router, prefix="/detalle_pedidos", tags=["detalle_pedidos"])
app.include_router(mesas_router, prefix="/mesas", tags=["mesas"])
