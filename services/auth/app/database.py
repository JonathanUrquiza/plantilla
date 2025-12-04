"""
Configuración de la base de datos.

Este archivo configura la conexión a PostgreSQL usando SQLAlchemy 2.0
con soporte asíncrono (asyncpg).

RECOMENDACIONES:
- Usar sesiones asíncronas para mejor rendimiento
- Implementar pool de conexiones apropiado
- Cerrar sesiones correctamente para evitar fugas
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool

from app.config import settings

# ==============================================================================
# CONFIGURACIÓN DEL ENGINE
# ==============================================================================
# El engine es la fuente de conexiones a la base de datos

engine = create_async_engine(
    settings.DATABASE_URL,
    # Pool de conexiones
    # En desarrollo puede usar NullPool para debugging
    # En producción usar configuración de pool apropiada
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    # Echo SQL queries (solo para debugging)
    echo=settings.DEBUG,
    # Reciclado de conexiones (evita conexiones obsoletas)
    pool_recycle=3600,  # 1 hora
    # Pre-ping para verificar conexiones
    pool_pre_ping=True,
)

# ==============================================================================
# CONFIGURACIÓN DE SESIONES
# ==============================================================================
# La sesión es el objeto que usamos para interactuar con la BD

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Evita queries extra después del commit
    autocommit=False,
    autoflush=False,
)

# ==============================================================================
# BASE PARA MODELOS
# ==============================================================================
# Todos los modelos heredan de esta clase

Base = declarative_base()


# ==============================================================================
# DEPENDENCY INJECTION PARA FASTAPI
# ==============================================================================

async def get_db() -> AsyncSession:
    """
    Dependency que provee una sesión de base de datos.
    
    Uso en routers:
        @router.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            # usar db aquí
            pass
    
    La sesión se cierra automáticamente al finalizar el request.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ==============================================================================
# FUNCIONES AUXILIARES
# ==============================================================================

async def init_db():
    """
    Inicializa la base de datos creando todas las tablas.
    
    Llamar al iniciar la aplicación o usar Alembic para migraciones.
    En producción, SIEMPRE usar Alembic.
    """
    async with engine.begin() as conn:
        # Crear todas las tablas
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """
    Cierra las conexiones a la base de datos.
    
    Llamar al cerrar la aplicación para liberar recursos.
    """
    await engine.dispose()


# ==============================================================================
# NOTAS PARA IMPLEMENTACIÓN
# ==============================================================================
"""
MIGRACIONES CON ALEMBIC:

1. Inicializar Alembic:
   $ alembic init alembic

2. Configurar alembic.ini y alembic/env.py con tu DATABASE_URL

3. Crear migración:
   $ alembic revision --autogenerate -m "descripción"

4. Aplicar migración:
   $ alembic upgrade head

5. Revertir migración:
   $ alembic downgrade -1


EJEMPLO DE MODELO:

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
"""

