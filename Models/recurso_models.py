# Archivo: Models/recurso_models.py
from pydantic import BaseModel

class RecursoCreate(BaseModel):
    tipo_recurso: str
    nombre: str
    funcionalidad: str

class RecursoUpdate(BaseModel):
    tipo_recurso: str = None
    nombre: str = None
    funcionalidad: str = None

class RecursoResponse(BaseModel):
    id_recurso: int
    tipo_recurso: str
    nombre: str
    funcionalidad: str
