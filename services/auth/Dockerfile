# ==============================================================================
# DOCKERFILE - SERVICIO DE AUTENTICACIÓN
# ==============================================================================
# Multi-stage build para imagen optimizada
#
# Stages:
# 1. builder: Instala dependencias
# 2. runtime: Imagen final mínima
#
# Build: docker build -t ecommerce-auth .
# Run: docker run -p 8001:8000 ecommerce-auth
# ==============================================================================

# ------------------------------------------------------------------------------
# STAGE 1: Builder
# ------------------------------------------------------------------------------
# Instala dependencias en una imagen con herramientas de build

FROM python:3.11-slim as builder

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero (para cache de Docker)
COPY requirements.txt .

# Crear virtual environment e instalar dependencias
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip && \
    pip install -r requirements.txt


# ------------------------------------------------------------------------------
# STAGE 2: Runtime
# ------------------------------------------------------------------------------
# Imagen final mínima solo con lo necesario para ejecutar

FROM python:3.11-slim as runtime

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Deshabilitar modo debug en producción
    DEBUG=false \
    # Puerto de la aplicación
    PORT=8000

# Crear usuario no-root por seguridad
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Instalar solo dependencias runtime necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# Copiar virtual environment desde builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copiar código de la aplicación
COPY ./app ./app

# Cambiar ownership al usuario no-root
RUN chown -R appuser:appgroup /app

# Cambiar a usuario no-root
USER appuser

# Exponer puerto
EXPOSE 8000

# Health check
# NOTA: Ajustar el endpoint según tu implementación
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando para ejecutar la aplicación
# Usar --host 0.0.0.0 para aceptar conexiones externas
# workers: ajustar según CPUs disponibles (recomendado: 2 * CPU + 1)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


# ==============================================================================
# NOTAS DE USO
# ==============================================================================
#
# DESARROLLO:
#   docker build -t ecommerce-auth .
#   docker run -p 8001:8000 --env-file .env ecommerce-auth
#
# PRODUCCIÓN (con más workers):
#   docker run -p 8001:8000 --env-file .env.prod ecommerce-auth \
#     uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
#
# CON DOCKER COMPOSE:
#   Ver docker-compose.yml en la carpeta infrastructure/
#
# ==============================================================================

