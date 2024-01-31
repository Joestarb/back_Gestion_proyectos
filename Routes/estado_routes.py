from fastapi import APIRouter, HTTPException, Body
from Config.database import connection
from Models.estado_models import Estado, EstadoCreate, EstadoUpdate

# Inicializar el router para la entidad 'estado'
estado_routes = APIRouter()

# Endpoint para crear un nuevo estado
@estado_routes.post("/estado/", response_model=Estado)
async def create_estado(estado_create: EstadoCreate = Body(...)):
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO estado (nombre) VALUES (%s)"
            values = (estado_create.nombre,)
            cursor.execute(query, values)
            connection.commit()

            estado_id = cursor.lastrowid
            return {"id_estado": estado_id, **estado_create.dict()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener todos los estados
@estado_routes.get("/estado/", response_model=list[Estado])
async def get_all_estados():
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM estado"
            cursor.execute(query)
            estados = cursor.fetchall()

            if estados:
                return estados
            else:
                raise HTTPException(status_code=404, detail="No estados found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener un estado por ID
@estado_routes.get("/estado/{estado_id}", response_model=Estado)
async def get_estado(estado_id: int):
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM estado WHERE id_estado = %s"
            cursor.execute(query, estado_id)
            estado = cursor.fetchone()

            if estado:
                return estado
            else:
                raise HTTPException(status_code=404, detail="Estado not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para actualizar un estado por ID
@estado_routes.put("/estado/{estado_id}", response_model=Estado)
async def update_estado(estado_id: int, estado_update: EstadoUpdate = Body(...)):
    try:
        with connection.cursor() as cursor:
            query = "UPDATE estado SET nombre = %s WHERE id_estado = %s"
            values = (estado_update.nombre, estado_id)
            cursor.execute(query, values)
            connection.commit()

            if cursor.rowcount > 0:
                return {"message": "Estado updated successfully", **estado_update.dict()}
            else:
                raise HTTPException(status_code=404, detail="Estado not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para eliminar un estado por ID
@estado_routes.delete("/estado/{estado_id}", response_model=dict)
async def delete_estado(estado_id: int):
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM estado WHERE id_estado = %s"
            cursor.execute(query, estado_id)
            connection.commit()

            if cursor.rowcount > 0:
                return {"message": "Estado deleted successfully"}
            else:
                raise HTTPException(status_code=404, detail="Estado not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
