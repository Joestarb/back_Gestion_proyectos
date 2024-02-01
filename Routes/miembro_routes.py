# Archivo: Models/miembro_routes.py
from fastapi import APIRouter, HTTPException, Body
from Config.database import connection
from Models.miebro_models import MiembroCreate, MiembroUpdate, MiembroResponse

miembro_router = APIRouter()

@miembro_router.post("/miembro/", response_model=MiembroResponse)
async def create_miembro(miembro: MiembroCreate = Body(...)):
    try:
        with connection.cursor() as cursor:
            query = """
                INSERT INTO miembro (nombre, correo_electronico, contrasena, fk_rol, fk_equipo)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (miembro.nombre, miembro.correo_electronico, miembro.contrasena, miembro.fk_rol, miembro.fk_equipo)
            cursor.execute(query, values)
            connection.commit()

            miembro_id = cursor.lastrowid
            return {"id_miembro": miembro_id, **miembro.dict()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@miembro_router.get("/miembro/", response_model=list[MiembroResponse])
async def get_all_miembros():
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM miembro"
            cursor.execute(query)
            miembros = cursor.fetchall()

            if miembros:
                return miembros
            else:
                raise HTTPException(status_code=404, detail="No miembros found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@miembro_router.get("/miembro/{miembro_id}", response_model=MiembroResponse)
async def get_miembro(miembro_id: int):
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM miembro WHERE id_miembro = %s"
            cursor.execute(query, miembro_id)
            miembro = cursor.fetchone()

            if miembro:
                return miembro
            else:
                raise HTTPException(status_code=404, detail="Miembro not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@miembro_router.put("/miembro/{miembro_id}", response_model=dict)
async def update_miembro(miembro_id: int, miembro_update: MiembroUpdate = Body(...)):
    try:
        with connection.cursor() as cursor:
            # Construir la consulta SQL de actualización dinámicamente
            update_fields = {k: v for k, v in miembro_update.dict(exclude_unset=True).items() if v is not None}
            if not update_fields:
                raise HTTPException(status_code=400, detail="No fields to update")

            set_clause = ", ".join([f"{field} = %s" for field in update_fields])
            query = f"UPDATE miembro SET {set_clause} WHERE id_miembro = %s"

            # Construir los valores para la consulta SQL
            values = list(update_fields.values()) + [miembro_id]

            cursor.execute(query, values)
            connection.commit()

            if cursor.rowcount > 0:
                return {"message": "Miembro updated successfully"}
            else:
                raise HTTPException(status_code=404, detail="Miembro not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@miembro_router.delete("/miembro/{miembro_id}", response_model=dict)
async def delete_miembro(miembro_id: int):
    try:
        with connection.cursor() as cursor:
            # Verificar si el miembro existe antes de intentar eliminarlo
            check_query = "SELECT * FROM miembro WHERE id_miembro = %s"
            cursor.execute(check_query, miembro_id)
            existing_miembro = cursor.fetchone()

            if not existing_miembro:
                raise HTTPException(status_code=404, detail="Miembro not found")

            # Eliminar el miembro
            delete_query = "DELETE FROM miembro WHERE id_miembro = %s"
            cursor.execute(delete_query, miembro_id)
            connection.commit()

            return {"message": "Miembro deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
