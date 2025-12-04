"""
Punto de entrada principal del servicio de autenticación.

Este archivo configura la aplicación FastAPI, incluye los routers,
configura CORS, middleware y eventos de inicio/cierre.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# TODO: Descomentar cuando implementes los routers
# from app.routers import auth_router
# from app.database import engine, Base
# from app.config import settings

# ==============================================================================
# CONFIGURACIÓN DE LIFESPAN (EVENTOS DE INICIO/CIERRE)
# ==============================================================================
# Aquí se configuran las acciones que se ejecutan al iniciar y cerrar
# la aplicación, como conexiones a base de datos, Redis, etc.

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestiona el ciclo de vida de la aplicación.
    
    INICIO (yield anterior):
    - Conectar a PostgreSQL
    - Conectar a Redis
    - Crear tablas si no existen
    - Cargar configuraciones
    
    CIERRE (yield posterior):
    - Cerrar conexiones a BD
    - Cerrar conexión a Redis
    - Limpiar recursos
    """
    # ==================== INICIO ====================
    print("🚀 Iniciando servicio de autenticación...")
    
    # TODO: Implementar conexión a base de datos
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    
    # TODO: Implementar conexión a Redis
    # app.state.redis = await aioredis.from_url(settings.REDIS_URL)
    
    print("✅ Servicio de autenticación iniciado correctamente")
    
    yield  # La aplicación se ejecuta aquí
    
    # ==================== CIERRE ====================
    print("🛑 Cerrando servicio de autenticación...")
    
    # TODO: Cerrar conexiones
    # await app.state.redis.close()
    
    print("✅ Servicio cerrado correctamente")


# ==============================================================================
# CONFIGURACIÓN DE LA APLICACIÓN FASTAPI
# ==============================================================================

app = FastAPI(
    title="Auth Service - Ecommerce",
    description="""
    ## Servicio de Autenticación
    
    Este microservicio maneja:
    - 🔐 Registro y login de usuarios
    - 🎫 Generación de JWT tokens
    - 🔄 Refresh tokens
    - 🌐 OAuth2 (Google, Facebook)
    - 📧 Verificación de email
    - 🔑 Reset de contraseña
    """,
    version="0.1.0",
    lifespan=lifespan,
    # TODO: Configurar URL de docs según entorno
    # docs_url="/docs" if settings.DEBUG else None,
    # redoc_url="/redoc" if settings.DEBUG else None,
)


# ==============================================================================
# CONFIGURACIÓN DE CORS
# ==============================================================================
# IMPORTANTE: En producción, configurar orígenes específicos

# TODO: Obtener orígenes de configuración
# origins = settings.CORS_ORIGINS

origins = [
    "http://localhost:3000",      # Frontend desarrollo
    "http://localhost:8080",      # Otro frontend
    # TODO: Agregar dominios de producción
    # "https://tu-ecommerce.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================================================================
# REGISTRO DE ROUTERS
# ==============================================================================
# Aquí se registran todos los routers del servicio

# TODO: Descomentar cuando implementes los routers
# app.include_router(
#     auth_router.router,
#     prefix="/auth",
#     tags=["Autenticación"]
# )


# ==============================================================================
# ENDPOINTS DE SALUD Y DIAGNÓSTICO
# ==============================================================================

@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raíz del servicio.
    Útil para verificar que el servicio está corriendo.
    """
    return {
        "service": "auth",
        "status": "running",
        "version": "0.1.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check para Docker y balanceadores de carga.
    
    RECOMENDACIÓN: Implementar verificaciones reales:
    - Conexión a PostgreSQL
    - Conexión a Redis
    - Otros servicios dependientes
    """
    # TODO: Implementar health checks reales
    # db_healthy = await check_database_connection()
    # redis_healthy = await check_redis_connection()
    
    return {
        "status": "healthy",
        "checks": {
            "database": "ok",      # TODO: Verificar conexión real
            "redis": "ok",         # TODO: Verificar conexión real
        }
    }


# ==============================================================================
# MANEJADORES DE ERRORES GLOBALES
# ==============================================================================
# TODO: Implementar manejadores de errores personalizados

# from fastapi import Request
# from fastapi.responses import JSONResponse
# 
# @app.exception_handler(CustomException)
# async def custom_exception_handler(request: Request, exc: CustomException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"detail": exc.detail}
#     )

