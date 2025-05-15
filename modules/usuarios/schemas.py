from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    correo: str
    contrasena: str
    estado: str = 'activo'
    numero_identificacion: str

class UsuarioCreate(UsuarioBase):
    pass  # Para la creación del usuario, puedes agregar validaciones adicionales si es necesario

class Usuario(UsuarioBase):
    id_usuario: int

    class Config:
        orm_mode = True  # Permite convertir el modelo SQLAlchemy a diccionario
