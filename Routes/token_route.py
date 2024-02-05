# auth_admin.py
from fastapi import HTTPException
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from Config.database import connection



SECRET_KEY = "4nDYuNhXqctKmRINu4uH6DDE68QS13crxvSobo5gFCg"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
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
