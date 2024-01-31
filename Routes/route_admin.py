from fastapi import HTTPException, APIRouter, Body
from Config.database import connection
from Models.admin_models import AdminCreate, AdminUpdate

# Inicializar la aplicación FastAPI
admin = APIRouter()

# Endpoint para crear un nuevo admin
@admin.post("/admin/", response_model=dict)
async def create_admin(admin: AdminCreate = Body(...)):
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO admin (nombre, correo_electronico, contrasena) VALUES (%s, %s, %s)"
            values = (admin.nombre, admin.correo_electronico, admin.contrasena)
            cursor.execute(query, values)
            connection.commit()

            admin_id = cursor.lastrowid
            return {"id_admin": admin_id, **admin.dict()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener todos los admins
@admin.get("/admin/", response_model=list)
async def get_all_admins():
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM admin"
            cursor.execute(query)
            admins = cursor.fetchall()

            if admins:
                return admins
            else:
                raise HTTPException(status_code=404, detail="No admins found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener un admin por ID
@admin.get("/admin/{admin_id}", response_model=dict)
async def get_admin(admin_id: int):
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM admin WHERE id_admin = %s"
            cursor.execute(query, admin_id)
            admin = cursor.fetchone()

            if admin:
                return admin
            else:
                raise HTTPException(status_code=404, detail="Admin not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para actualizar un admin por ID
@admin.put("/admin/{admin_id}", response_model=dict)
async def update_admin(admin_id: int, admin_update: AdminUpdate = Body(...)):
    try:
        with connection.cursor() as cursor:
            # Construir la consulta SQL de actualización dinámicamente
            update_fields = {k: v for k, v in admin_update.dict(exclude_unset=True).items() if v is not None}
            if not update_fields:
                raise HTTPException(status_code=400, detail="No fields to update")

            set_clause = ", ".join([f"{field} = %s" for field in update_fields])
            query = f"UPDATE admin SET {set_clause} WHERE id_admin = %s"

            # Construir los valores para la consulta SQL
            values = list(update_fields.values())
            values.append(admin_id)

            cursor.execute(query, values)
            connection.commit()

            if cursor.rowcount > 0:
                return {"message": "Admin updated successfully"}
            else:
                raise HTTPException(status_code=404, detail="Admin not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para eliminar un admin por ID
@admin.delete("/admin/{admin_id}", response_model=dict)
async def delete_admin(admin_id: int):
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM admin WHERE id_admin = %s"
            cursor.execute(query, admin_id)
            connection.commit()

            if cursor.rowcount > 0:
                return {"message": "Admin deleted successfully"}
            else:
                raise HTTPException(status_code=404, detail="Admin not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
