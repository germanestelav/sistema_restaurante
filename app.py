# app.py
from fastapi import FastAPI
from modules.usuarios.routes import router as usuarios_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API ERP"}

# Incluir las rutas de usuario
app.include_router(usuarios_router, prefix="/usuarios", tags=["usuarios"])
