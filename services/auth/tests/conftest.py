"""
Fixtures compartidos para tests.

Los fixtures se cargan automáticamente en todos los tests.
Proveen configuración común como:
- Cliente de prueba
- Sesión de BD de prueba
- Usuarios de prueba
"""

import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

# TODO: Importar cuando estén implementados
# from app.main import app
# from app.database import Base, get_db
# from app.config import settings


# ==============================================================================
# CONFIGURACIÓN DE PYTEST-ASYNCIO
# ==============================================================================

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """
    Crea un event loop para toda la sesión de tests.
    
    Necesario para tests asíncronos con pytest-asyncio.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ==============================================================================
# FIXTURES DE BASE DE DATOS
# ==============================================================================

# URL de BD de prueba (usar BD separada o SQLite en memoria)
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
# Para PostgreSQL de prueba:
# TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/auth_test"


@pytest_asyncio.fixture(scope="function")
async def db_engine():
    """
    Crea un engine de BD para tests.
    
    Usa NullPool para evitar problemas con conexiones compartidas.
    """
    # TODO: Descomentar cuando implementes
    # engine = create_async_engine(
    #     TEST_DATABASE_URL,
    #     poolclass=NullPool,
    #     echo=False
    # )
    # 
    # # Crear tablas
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    # 
    # yield engine
    # 
    # # Limpiar tablas después de cada test
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    # 
    # await engine.dispose()
    yield None


@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Provee una sesión de BD para cada test.
    
    La sesión se hace rollback después de cada test para
    mantener los tests aislados.
    """
    # TODO: Descomentar cuando implementes
    # async_session = async_sessionmaker(
    #     db_engine,
    #     class_=AsyncSession,
    #     expire_on_commit=False
    # )
    # 
    # async with async_session() as session:
    #     yield session
    #     await session.rollback()
    yield None


# ==============================================================================
# FIXTURES DE CLIENTE HTTP
# ==============================================================================

@pytest_asyncio.fixture(scope="function")
async def client(db_session) -> AsyncGenerator[AsyncClient, None]:
    """
    Cliente HTTP para tests de endpoints.
    
    Usa la sesión de BD de prueba en lugar de la real.
    """
    # TODO: Descomentar cuando implementes
    # 
    # # Override de la dependencia de BD
    # async def override_get_db():
    #     yield db_session
    # 
    # app.dependency_overrides[get_db] = override_get_db
    # 
    # async with AsyncClient(app=app, base_url="http://test") as ac:
    #     yield ac
    # 
    # app.dependency_overrides.clear()
    yield None


# ==============================================================================
# FIXTURES DE USUARIOS
# ==============================================================================

@pytest_asyncio.fixture
async def test_user(db_session):
    """
    Crea un usuario de prueba en la BD.
    
    Retorna el usuario creado para usar en tests.
    """
    # TODO: Implementar cuando tengas los modelos
    # 
    # from app.models.user import User, UserCredential, AuthProvider
    # from app.utils.security import hash_password
    # 
    # user = User(
    #     email="test@example.com",
    #     is_active=True,
    #     is_verified=True
    # )
    # db_session.add(user)
    # await db_session.flush()
    # 
    # credential = UserCredential(
    #     user_id=user.id,
    #     provider=AuthProvider.LOCAL,
    #     hashed_password=hash_password("TestPassword123")
    # )
    # db_session.add(credential)
    # await db_session.commit()
    # 
    # return user
    return None


@pytest_asyncio.fixture
async def test_admin(db_session):
    """
    Crea un usuario admin de prueba.
    """
    # TODO: Similar a test_user pero con role=admin
    return None


@pytest_asyncio.fixture
async def auth_headers(test_user):
    """
    Genera headers de autenticación para un usuario de prueba.
    
    Útil para tests de endpoints protegidos.
    
    Uso:
        async def test_protected_endpoint(client, auth_headers):
            response = await client.get("/me", headers=auth_headers)
            assert response.status_code == 200
    """
    # TODO: Implementar cuando tengas TokenService
    # 
    # from app.services.token_service import TokenService
    # 
    # token_service = TokenService()
    # access_token = token_service.create_access_token(test_user)
    # 
    # return {"Authorization": f"Bearer {access_token}"}
    return {}


# ==============================================================================
# FIXTURES DE DATOS DE PRUEBA
# ==============================================================================

@pytest.fixture
def valid_user_data() -> dict:
    """
    Datos válidos para registro de usuario.
    """
    return {
        "email": "newuser@example.com",
        "password": "SecurePassword123",
        "password_confirm": "SecurePassword123"
    }


@pytest.fixture
def valid_login_data() -> dict:
    """
    Datos válidos para login.
    """
    return {
        "email": "test@example.com",
        "password": "TestPassword123"
    }


@pytest.fixture
def invalid_login_data() -> dict:
    """
    Datos inválidos para login.
    """
    return {
        "email": "test@example.com",
        "password": "WrongPassword"
    }

