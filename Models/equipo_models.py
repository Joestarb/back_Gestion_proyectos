# Archivo: Models/equipo_models.py
from pydantic import BaseModel

# Define la clase para la creación de un nuevo equipo
class EquipoCreate(BaseModel):
    nombre: str

# Define la clase para la actualización de un equipo existente
class EquipoUpdate(BaseModel):
    nombre: str = None
