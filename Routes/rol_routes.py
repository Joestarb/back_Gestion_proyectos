# Archivo: Models/rol_routes.py
from fastapi import APIRouter, HTTPException, Body
from Config.database import connection
from Models.rol_model import RolCreate, RolUpdate, RolResponse

rol_router = APIRouter()

@rol_router.post("/rol/", response_model=RolResponse)
async def create_rol(rol: RolCreate = Body(...)):
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO rol (nombre) VALUES (%s)"
            values = (rol.nombre,)
            cursor.execute(query, values)
            connection.commit()

            rol_id = cursor.lastrowid
            return {"id_rol": rol_id, **rol.dict()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@rol_router.get("/rol/", response_model=list[RolResponse])
async def get_all_roles():
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM rol"
            cursor.execute(query)
            roles = cursor.fetchall()

            if roles:
                return roles
            else:
                raise HTTPException(status_code=404, detail="No roles found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@rol_router.get("/rol/{rol_id}", response_model=RolResponse)
async def get_rol(rol_id: int):
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM rol WHERE id_rol = %s"
            cursor.execute(query, rol_id)
            rol = cursor.fetchone()

            if rol:
                return rol
            else:
                raise HTTPException(status_code=404, detail="Rol not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@rol_router.put("/rol/{rol_id}", response_model=RolResponse)
async def update_rol(rol_id: int, rol_update: RolUpdate = Body(...)):
    try:
        with connection.cursor() as cursor:
            update_fields = {k: v for k, v in rol_update.dict(exclude_unset=True).items() if v is not None}
            if not update_fields:
                raise HTTPException(status_code=400, detail="No fields to update")

            set_clause = ", ".join([f"{field} = %s" for field in update_fields])
            query = f"UPDATE rol SET {set_clause} WHERE id_rol = %s"

            values = list(update_fields.values())
            values.append(rol_id)

            cursor.execute(query, values)
            connection.commit()

            if cursor.rowcount > 0:
                return {"message": "Rol updated successfully"}
            else:
                raise HTTPException(status_code=404, detail="Rol not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@rol_router.delete("/rol/{rol_id}", response_model=dict)
async def delete_rol(rol_id: int):
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM rol WHERE id_rol = %s"
            cursor.execute(query, rol_id)
            connection.commit()

            if cursor.rowcount > 0:
                return {"message": "Rol deleted successfully"}
            else:
                raise HTTPException(status_code=404, detail="Rol not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
