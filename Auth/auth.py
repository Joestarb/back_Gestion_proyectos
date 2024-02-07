# auth.py

from fastapi import HTTPException
from passlib.context import CryptContext
from jose import JWTError, jwt
from Config.database import connection
from Models.admin_models import AdminCreate, AdminUpdate
from datetime import datetime, timedelta


SECRET_KEY = "4nDYuNhXqctKmRINu4uH6DDE68QS13crxvSobo5gFCg"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def create_access_token(data: dict, expires_delta: timedelta, rol: str = "admin"):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "rol": rol})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def hash_password(password: str):
    return pwd_context.hash(password)

def authenticate_admin(email: str, password: str):
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM admin WHERE correo_electronico = %s"
            cursor.execute(query, email)
            admin = cursor.fetchone()

            if admin and pwd_context.verify(password, admin['contrasena']):
                return admin
            else:
                return None

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
