from pydantic import BaseModel

# Define la clase para la creación de un nuevo admin
class AdminCreate(BaseModel):
    nombre: str
    correo_electronico: str
    contrasena: str

# Define la clase para la actualización de un admin existente
class AdminUpdate(BaseModel):
    nombre: str = None
    correo_electronico: str = None
    contrasena: str = None
