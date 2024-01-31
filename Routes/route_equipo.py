from fastapi import APIRouter, HTTPException, Body
from Config.database import connection
from Models.equipo_models import EquipoCreate, EquipoUpdate

# Inicializar el equipo para los equipos
equipo = APIRouter()

# Endpoint para crear un nuevo equipo
@equipo.post("/equipo/", response_model=dict)
async def create_equipo(equipo: EquipoCreate = Body(...)):
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO equipo (nombre) VALUES (%s)"
            values = (equipo.nombre,)
            cursor.execute(query, values)
            connection.commit()

            equipo_id = cursor.lastrowid
            return {"id_equipo": equipo_id, **equipo.dict()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener todos los equipos
@equipo.get("/equipo/", response_model=list)
async def get_all_equipos():
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM equipo"
            cursor.execute(query)
            equipos = cursor.fetchall()

            if equipos:
                return equipos
            else:
                raise HTTPException(status_code=404, detail="No equipos found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener un equipo por ID
@equipo.get("/equipo/{equipo_id}", response_model=dict)
async def get_equipo(equipo_id: int):
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM equipo WHERE id_equipo = %s"
            cursor.execute(query, equipo_id)
            equipo = cursor.fetchone()

            if equipo:
                return equipo
            else:
                raise HTTPException(status_code=404, detail="Equipo not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para actualizar un equipo por ID
@equipo.put("/equipo/{equipo_id}", response_model=dict)
async def update_equipo(equipo_id: int, equipo_update: EquipoUpdate = Body(...)):
    try:
        with connection.cursor() as cursor:
            update_fields = {k: v for k, v in equipo_update.dict(exclude_unset=True).items() if v is not None}
            if not update_fields:
                raise HTTPException(status_code=400, detail="No fields to update")

            set_clause = ", ".join([f"{field} = %s" for field in update_fields])
            query = f"UPDATE equipo SET {set_clause} WHERE id_equipo = %s"

            values = list(update_fields.values())
            values.append(equipo_id)

            cursor.execute(query, values)
            connection.commit()

            if cursor.rowcount > 0:
                return {"message": "Equipo updated successfully"}
            else:
                raise HTTPException(status_code=404, detail="Equipo not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para eliminar un equipo por ID
@equipo.delete("/equipo/{equipo_id}", response_model=dict)
async def delete_equipo(equipo_id: int):
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM equipo WHERE id_equipo = %s"
            cursor.execute(query, equipo_id)
            connection.commit()

            if cursor.rowcount > 0:
                return {"message": "Equipo deleted successfully"}
            else:
                raise HTTPException(status_code=404, detail="Equipo not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))