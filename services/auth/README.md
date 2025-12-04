# 🔐 Auth Service

Servicio de autenticación para el ecommerce.

## 📋 Descripción

Este microservicio maneja toda la autenticación y autorización del sistema:

- Registro de usuarios
- Login/Logout
- Tokens JWT (access + refresh)
- OAuth2 (Google, Facebook)
- Reset de password
- Verificación de email

## 🚀 Inicio Rápido

### Prerequisitos

- Python 3.11+
- PostgreSQL
- Redis

### Instalación

```bash
# Crear virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Copiar variables de entorno
cp .env.example .env
# Editar .env con tus valores
```

### Configurar Base de Datos

```bash
# Crear base de datos
createdb auth_db

# Ejecutar migraciones (cuando implementes Alembic)
alembic upgrade head
```

### Ejecutar

```bash
# Desarrollo (con hot reload)
uvicorn app.main:app --reload --port 8001

# Producción
uvicorn app.main:app --host 0.0.0.0 --port 8001 --workers 4
```

### Con Docker

```bash
# Build
docker build -t ecommerce-auth .

# Run
docker run -p 8001:8000 --env-file .env ecommerce-auth
```

## 📚 API Docs

Una vez ejecutando, acceder a:

- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## 🔌 Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/auth/register` | Registrar usuario |
| POST | `/auth/login` | Iniciar sesión |
| POST | `/auth/logout` | Cerrar sesión |
| POST | `/auth/refresh` | Renovar access token |
| GET | `/auth/me` | Obtener usuario actual |
| POST | `/auth/password/reset` | Solicitar reset |
| POST | `/auth/password/reset/confirm` | Confirmar reset |
| POST | `/auth/password/change` | Cambiar password |
| GET | `/auth/verify/{token}` | Verificar email |
| GET | `/auth/oauth/google` | Login con Google |
| GET | `/auth/oauth/facebook` | Login con Facebook |

## 🧪 Tests

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar tests
pytest

# Con coverage
pytest --cov=app --cov-report=html

# Ver reporte de coverage
open htmlcov/index.html
```

## 📁 Estructura

```
auth/
├── app/
│   ├── __init__.py         # Descripción del servicio
│   ├── main.py             # Punto de entrada FastAPI
│   ├── config.py           # Configuración
│   ├── database.py         # Conexión a BD
│   ├── models/             # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/            # Schemas Pydantic
│   │   ├── __init__.py
│   │   └── auth.py
│   ├── routers/            # Endpoints
│   │   ├── __init__.py
│   │   └── auth_router.py
│   ├── services/           # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── token_service.py
│   └── utils/              # Utilidades
│       ├── __init__.py
│       ├── security.py
│       └── dependencies.py
├── tests/                  # Tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_services.py
├── Dockerfile
├── requirements.txt
├── requirements-dev.txt
├── .env.example
└── README.md
```

## 🔧 Variables de Entorno

Ver `.env.example` para la lista completa.

Variables críticas:
- `SECRET_KEY`: Clave para JWT (cambiar en producción)
- `DATABASE_URL`: URL de PostgreSQL
- `REDIS_URL`: URL de Redis

## 📝 TODO

- [ ] Implementar registro de usuarios
- [ ] Implementar login/logout
- [ ] Implementar generación de JWT
- [ ] Implementar refresh tokens
- [ ] Implementar OAuth2 con Google
- [ ] Implementar OAuth2 con Facebook
- [ ] Implementar reset de password
- [ ] Implementar verificación de email
- [ ] Agregar rate limiting
- [ ] Configurar Alembic para migraciones

