# Archivo: Models/miembro_models.py
from pydantic import BaseModel

class MiembroCreate(BaseModel):
    nombre: str
    correo_electronico: str
    contrasena: str
    fk_rol: int
    fk_equipo: int

class MiembroUpdate(BaseModel):
    nombre: str = None
    correo_electronico: str = None
    contrasena: str = None
    fk_rol: int = None
    fk_equipo: int = None

class MiembroResponse(BaseModel):
    id_miembro: int
    nombre: str
    correo_electronico: str
    fk_rol: int
    fk_equipo: int
