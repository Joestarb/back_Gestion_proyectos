from fastapi import APIRouter, HTTPException, Body
from Config.database import connection
from Models.proyecto_models import Proyecto, ProyectoCreate, ProyectoUpdate

proyecto_routes = APIRouter()

@proyecto_routes.get("/proyecto/miembro/{miembro_id}", response_model=list[Proyecto])
async def get_proyectos_by_miembro(miembro_id: int):
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT p.*
                FROM proyecto p
                JOIN miembro_proyecto mp ON p.id_proyecto = mp.fk_proyecto
                JOIN miembro m ON mp.fk_miembro = m.id_miembro
                WHERE m.id_miembro = %s
            """
            cursor.execute(query, miembro_id)
            proyectos = cursor.fetchall()

            if proyectos:
                return proyectos
            else:
                raise HTTPException(status_code=404, detail=f"No projects found for member with id {miembro_id}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@proyecto_routes.post("/proyecto/", response_model=Proyecto)
async def create_proyecto(proyecto_create: ProyectoCreate = Body(...)):
    try:
        with connection.cursor() as cursor:
            query = """
                INSERT INTO proyecto (nombre, descripcion, fecha_inicio, fk_equipo, fk_estado, fk_recurso)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                proyecto_create.nombre,
                proyecto_create.descripcion,
                proyecto_create.fecha_inicio,
                proyecto_create.fk_equipo,
                proyecto_create.fk_estado,
                proyecto_create.fk_recurso,
            )
            cursor.execute(query, values)
            connection.commit()

            proyecto_id = cursor.lastrowid
            return {"id_proyecto": proyecto_id, **proyecto_create.dict()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@proyecto_routes.get("/proyecto/{proyecto_id}", response_model=Proyecto)
async def get_proyecto(proyecto_id: int):
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM proyecto WHERE id_proyecto = %s"
            cursor.execute(query, proyecto_id)
            proyecto = cursor.fetchone()

            if proyecto:
                return proyecto
            else:
                raise HTTPException(status_code=404, detail="Proyecto not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@proyecto_routes.put("/proyecto/{proyecto_id}", response_model=Proyecto)
async def update_proyecto(proyecto_id: int, proyecto_update: ProyectoUpdate = Body(...)):
    try:
        with connection.cursor() as cursor:
            query = """
                UPDATE proyecto
                SET nombre = %s, descripcion = %s, fecha_inicio = %s, fk_equipo = %s, fk_estado = %s, fk_recurso = %s
                WHERE id_proyecto = %s
            """
            values = (
                proyecto_update.nombre,
                proyecto_update.descripcion,
                proyecto_update.fecha_inicio,
                proyecto_update.fk_equipo,
                proyecto_update.fk_estado,
                proyecto_update.fk_recurso,
                proyecto_id,
            )
            cursor.execute(query, values)
            connection.commit()

            if cursor.rowcount > 0:
                # Devuelve el objeto Pydantic con el id_proyecto
                return Proyecto(id_proyecto=proyecto_id, **proyecto_update.dict())
            else:
                raise HTTPException(status_code=404, detail="Proyecto not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    try:
        with connection.cursor() as cursor:
            query = """
                UPDATE proyecto
                SET nombre = %s, descripcion = %s, fecha_inicio = %s, fk_equipo = %s, fk_estado = %s, fk_recurso = %s
                WHERE id_proyecto = %s
            """
            values = (
                proyecto_update.nombre,
                proyecto_update.descripcion,
                proyecto_update.fecha_inicio,
                proyecto_update.fk_equipo,
                proyecto_update.fk_estado,
                proyecto_update.fk_recurso,
                proyecto_id,
            )
            cursor.execute(query, values)
            connection.commit()

            if cursor.rowcount > 0:
                return {"message": "Proyecto updated successfully", **proyecto_update.dict()}
            else:
                raise HTTPException(status_code=404, detail="Proyecto not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@proyecto_routes.get("/proyecto/", response_model=list[Proyecto])
async def get_all_proyectos():
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM proyecto"
            cursor.execute(query)
            proyectos = cursor.fetchall()

            if proyectos:
             return proyectos
            else:
             return []


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@proyecto_routes.delete("/proyecto/{proyecto_id}", response_model=dict)
async def delete_proyecto(proyecto_id: int):
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM proyecto WHERE id_proyecto = %s"
            cursor.execute(query, proyecto_id)
            connection.commit()

            if cursor.rowcount > 0:
                return {"message": "Proyecto deleted successfully"}
            else:
                raise HTTPException(status_code=404, detail="Proyecto not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))