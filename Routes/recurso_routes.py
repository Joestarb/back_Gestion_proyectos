# Archivo: Models/recurso_routes.py
from fastapi import APIRouter, HTTPException, Body
from Config.database import connection
from Models.recurso_models import RecursoCreate, RecursoUpdate, RecursoResponse

recurso_router = APIRouter()

@recurso_router.post("/recurso/", response_model=RecursoResponse)
async def create_recurso(recurso: RecursoCreate = Body(...)):
    try:
        with connection.cursor() as cursor:
            query = """
                INSERT INTO recurso (tipo_recurso, nombre, funcionalidad)
                VALUES (%s, %s, %s)
            """
            values = (recurso.tipo_recurso, recurso.nombre, recurso.funcionalidad)
            cursor.execute(query, values)
            connection.commit()

            recurso_id = cursor.lastrowid
            return {"id_recurso": recurso_id, **recurso.dict()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@recurso_router.get("/recurso/", response_model=list[RecursoResponse])
async def get_all_recursos():
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM recurso"
            cursor.execute(query)
            recursos = cursor.fetchall()

            if recursos:
                return recursos
            else:
                raise HTTPException(status_code=404, detail="No recursos found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@recurso_router.get("/recurso/{recurso_id}", response_model=RecursoResponse)
async def get_recurso(recurso_id: int):
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM recurso WHERE id_recurso = %s"
            cursor.execute(query, recurso_id)
            recurso = cursor.fetchone()

            if recurso:
                return recurso
            else:
                raise HTTPException(status_code=404, detail="Recurso not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@recurso_router.put("/recurso/{recurso_id}", response_model=RecursoResponse)
async def update_recurso(recurso_id: int, recurso_update: RecursoUpdate = Body(...)):
    try:
        with connection.cursor() as cursor:
            update_fields = {k: v for k, v in recurso_update.dict(exclude_unset=True).items() if v is not None}
            if not update_fields:
                raise HTTPException(status_code=400, detail="No fields to update")

            set_clause = ", ".join([f"{field} = %s" for field in update_fields])
            query = f"UPDATE recurso SET {set_clause} WHERE id_recurso = %s"

            values = list(update_fields.values())
            values.append(recurso_id)

            cursor.execute(query, values)
            connection.commit()

            if cursor.rowcount > 0:
                return {"message": "Recurso updated successfully"}
            else:
                raise HTTPException(status_code=404, detail="Recurso not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@recurso_router.delete("/recurso/{recurso_id}", response_model=dict)
async def delete_recurso(recurso_id: int):
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM recurso WHERE id_recurso = %s"
            cursor.execute(query, recurso_id)
            connection.commit()

            if cursor.rowcount > 0:
                return {"message": "Recurso deleted successfully"}
            else:
                raise HTTPException(status_code=404, detail="Recurso not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
