from fastapi import FastAPI
from Routes.route_equipo import equipo
from Routes.route_admin import admin
from Routes.rol_routes import rol_router
from Routes.miembro_routes import miembro_router
from Routes.recurso_routes import recurso_router
from Routes.estado_routes import estado_routes



from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# Configuración para permitir todos los orígenes, todos los métodos y encabezados específicos
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Añade los routers de los controladores a tu aplicación
app.include_router(admin)
app.include_router(equipo)
app.include_router(rol_router)
app.include_router(miembro_router)
app.include_router(recurso_router)
app.include_router(recurso_router)
app.include_router(estado_routes)





