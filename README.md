# 🛒 Backend Ecommerce - Plantilla de Microservicios

Plantilla completa de backend para un ecommerce con arquitectura de microservicios.

## 📋 Características

- ✅ **Arquitectura de Microservicios** - Servicios independientes y escalables
- ✅ **FastAPI** - Framework Python moderno y de alto rendimiento
- ✅ **PostgreSQL** - Base de datos robusta con soporte ACID
- ✅ **Redis** - Cache y almacenamiento de sesiones
- ✅ **Docker** - Containerización completa
- ✅ **OAuth2 + JWT** - Autenticación segura
- ✅ **MercadoPago** - Integración de pagos para LATAM
- ✅ **GitHub Actions** - CI/CD automatizado
- ✅ **Tests** - Pytest con unit e integration tests

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND                                    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           API GATEWAY                                    │
│                    (Nginx / Kong / AWS ALB)                              │
└─────────────────────────────────────────────────────────────────────────┘
          │           │           │           │           │
          ▼           ▼           ▼           ▼           ▼
     ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
     │  Auth  │  │ Users  │  │Products│  │  Cart  │  │ Orders │
     │ :8001  │  │ :8002  │  │ :8003  │  │ :8004  │  │ :8005  │
     └────────┘  └────────┘  └────────┘  └────────┘  └────────┘
          │           │           │           │           │
          └───────────┴───────────┴───────────┴───────────┘
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          ▼                         ▼                         ▼
     ┌────────┐               ┌──────────┐              ┌──────────┐
     │Payments│               │PostgreSQL│              │  Redis   │
     │ :8006  │               │  :5432   │              │  :6379   │
     └────────┘               └──────────┘              └──────────┘
          │
          ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│    Shipping     │  │  Notifications  │  │    Downloads    │
│     :8007       │  │     :8008       │  │     :8009       │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

## 📦 Microservicios

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| **Auth** | 8001 | Autenticación OAuth2/JWT |
| **Users** | 8002 | Gestión de usuarios y perfiles |
| **Products** | 8003 | Catálogo e inventario |
| **Cart** | 8004 | Carrito de compras (Redis) |
| **Orders** | 8005 | Gestión de pedidos |
| **Payments** | 8006 | Integración MercadoPago |
| **Shipping** | 8007 | Envíos y direcciones |
| **Notifications** | 8008 | Emails y notificaciones |
| **Downloads** | 8009 | Productos digitales |

## 🚀 Inicio Rápido

### Prerequisitos

- Python 3.11+
- Docker y Docker Compose
- PostgreSQL 15+ (o usar Docker)
- Redis 7+ (o usar Docker)

### 1. Clonar y configurar

```bash
# Clonar repositorio
git clone <url-del-repo>
cd backend-plantilla

# Copiar variables de entorno
cp infrastructure/.env.example infrastructure/.env
# Editar .env con tus valores
```

### 2. Levantar infraestructura

```bash
cd infrastructure

# Levantar PostgreSQL y Redis
docker-compose up -d postgres redis

# Verificar que están corriendo
docker-compose ps
```

### 3. Iniciar un servicio

```bash
cd services/auth

# Crear virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones (cuando implementes Alembic)
# alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload --port 8001
```

### 4. Ver documentación API

- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## 📁 Estructura del Proyecto

```
backend-plantilla/
├── docs/                          # Documentación
│   ├── ENCUESTA_REQUISITOS.md     # Requisitos del proyecto
│   ├── RECOMENDACIONES.md         # Guía de implementación
│   └── PROXIMOS_PASOS.md          # Checklist de tareas
│
├── infrastructure/                # Infraestructura
│   ├── docker-compose.yml         # Desarrollo local
│   └── scripts/                   # Scripts de setup
│
├── services/                      # Microservicios
│   ├── auth/                      # Servicio de autenticación
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── models/
│   │   │   ├── schemas/
│   │   │   ├── routers/
│   │   │   ├── services/
│   │   │   └── utils/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── users/                     # Servicio de usuarios
│   ├── products/                  # Servicio de productos
│   ├── cart/                      # Servicio de carrito
│   ├── orders/                    # Servicio de órdenes
│   ├── payments/                  # Servicio de pagos
│   ├── shipping/                  # Servicio de envíos
│   ├── notifications/             # Servicio de notificaciones
│   └── downloads/                 # Servicio de descargas
│
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI/CD
│
├── .gitignore
└── README.md
```

## 🔧 Stack Tecnológico

| Categoría | Tecnología |
|-----------|------------|
| Lenguaje | Python 3.11 |
| Framework | FastAPI |
| Base de datos | PostgreSQL 15 |
| Cache | Redis 7 |
| ORM | SQLAlchemy 2.0 |
| Migraciones | Alembic |
| Autenticación | OAuth2 + JWT |
| Pagos | MercadoPago |
| Tests | pytest |
| Containers | Docker |
| CI/CD | GitHub Actions |

## 📝 Documentación

- **[Encuesta de Requisitos](docs/ENCUESTA_REQUISITOS.md)** - Decisiones de arquitectura
- **[Recomendaciones](docs/RECOMENDACIONES.md)** - Guía de implementación
- **[Próximos Pasos](docs/PROXIMOS_PASOS.md)** - Checklist de tareas

## 🧪 Testing

```bash
cd services/auth

# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar tests
pytest

# Con coverage
pytest --cov=app --cov-report=html
```

## 🐳 Docker

### Desarrollo

```bash
cd infrastructure
docker-compose up -d
```

### Producción

```bash
cd infrastructure
docker-compose -f docker-compose.prod.yml up -d
```

## 🔐 Variables de Entorno

Cada servicio requiere configuración. Ver los archivos `env.example` en cada servicio.

Variables críticas:
- `SECRET_KEY` - Clave para JWT (cambiar en producción!)
- `DATABASE_URL` - Conexión a PostgreSQL
- `REDIS_URL` - Conexión a Redis
- `MERCADOPAGO_ACCESS_TOKEN` - Token de MercadoPago

## 🤝 Contribuir

1. Fork el proyecto
2. Crear branch (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push al branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto es una plantilla para uso personal/comercial.

---

Desarrollado con ❤️ para facilitar la creación de ecommerce con microservicios.

#   p l a n t i l l a  
 