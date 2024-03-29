from pydantic import BaseModel

class EstadoBase(BaseModel):
    nombre: str

class EstadoCreate(EstadoBase):
    pass

class EstadoUpdate(EstadoBase):
    pass

class EstadoInDBBase(EstadoBase):
    id_estado: int

    class Config:
        from_attributes = True

class Estado(EstadoInDBBase):
    pass
