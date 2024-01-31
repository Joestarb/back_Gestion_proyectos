# Archivo: Models/rol_models.py
from pydantic import BaseModel

class RolCreate(BaseModel):
    nombre: str

class RolUpdate(BaseModel):
    nombre: str = None

class RolResponse(BaseModel):
    id_rol: int
    nombre: str

