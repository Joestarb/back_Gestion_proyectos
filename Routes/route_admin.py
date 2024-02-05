from fastapi import APIRouter, HTTPException, Body
from Config.database import connection
from Models.admin_models import AdminCreate, AdminUpdate
from Routes.token_route import  create_access_token, authenticate_admin, hash_password
from datetime import datetime, timedelta
# Inicializar la aplicación FastAPI
admin = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# Endpoint para crear un nuevo admin
# Endpoint para iniciar sesión y obtener un token de acceso
@admin.post("/token", response_model=dict)
async def login_for_access_token(form_data: AdminCreate = Body(...)):
    admin_data = authenticate_admin(form_data.correo_electronico, form_data.contrasena)

    if admin_data:
        # Generar token de acceso
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": admin_data['correo_electronico']}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# Endpoint para crear un nuevo admin
@admin.post("/admin/", response_model=dict)
async def create_admin(admin: AdminCreate = Body(...)):
    try:
        with connection.cursor() as cursor:
            # Hashear la contraseña antes de almacenarla en la base de datos
            hashed_password = hash_password(admin.contrasena)

            query = "INSERT INTO admin (nombre, correo_electronico, contrasena) VALUES (%s, %s, %s)"
            values = (admin.nombre, admin.correo_electronico, hashed_password)
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
