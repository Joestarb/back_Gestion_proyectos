from pydantic import BaseModel, Field
from datetime import date

class ProyectoBase(BaseModel):
    nombre: str = Field(..., title="Nombre del proyecto", max_length=255)
    descripcion: str = Field(..., title="Descripción del proyecto", max_length=255)
    fecha_inicio: date = Field(..., title="Fecha de inicio del proyecto")
    fk_equipo: int = Field(..., title="ID del equipo asociado al proyecto")
    fk_estado: int = Field(..., title="ID del estado asociado al proyecto")
    fk_recurso: int = Field(..., title="ID del recurso asociado al proyecto")

class ProyectoCreate(ProyectoBase):
    pass

class ProyectoUpdate(ProyectoBase):
    pass

class ProyectoInDBBase(ProyectoBase):
    id_proyecto: int

    class Config:
        orm_mode = True

class Proyecto(ProyectoInDBBase):
    pass
