# auth_member.py
from fastapi import HTTPException
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from Config.database import connection

SECRET_KEY_MEMBER = "4nDYuNhXqctKmRINu4uH6DDE68QS13crxvSobo5gFCg"  # Replace with a secure secret key
ALGORITHM_MEMBER = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES_MEMBER = 30

pwd_context_member = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token_member(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_MEMBER, algorithm=ALGORITHM_MEMBER)
    return encoded_jwt

def hash_password_member(password: str):
    return pwd_context_member.hash(password)

def authenticate_member(email: str, password: str):
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM miembro WHERE correo_electronico = %s"
            cursor.execute(query, email)
            member = cursor.fetchone()

            if member and pwd_context_member.verify(password, member['contrasena']):
                return member
            else:
                return None

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
