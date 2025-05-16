from datetime import datetime, timedelta
from jose import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY", "CAMBIA_ESTO_EN_PRODUCCION")
ALGORITHM = "HS256"
RESET_TOKEN_EXPIRE_MINUTES = 30

def crear_token_reset(email: str):
    expire = datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token_reset(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except Exception:
        return None

def enviar_email_reset(email: str, token: str):
    # Aquí deberías integrar un servicio real de correo (SMTP, SendGrid, etc.)
    print(f"Enlace de recuperación para {email}: http://localhost:8000/password-reset/confirm?token={token}")