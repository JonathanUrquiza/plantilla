"""
Configuración del servicio de autenticación.

Este archivo centraliza toda la configuración del servicio,
cargando valores desde variables de entorno usando Pydantic Settings.

IMPORTANTE: Las variables sensibles (SECRET_KEY, DATABASE_URL, etc.)
NUNCA deben estar hardcodeadas. Siempre usar variables de entorno.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Configuración del servicio cargada desde variables de entorno.
    
    Las variables se cargan automáticamente desde:
    1. Variables de entorno del sistema
    2. Archivo .env (si existe)
    
    Todas las variables con valores por defecto pueden ser
    sobrescritas en producción.
    """
    
    # =========================================================================
    # CONFIGURACIÓN GENERAL
    # =========================================================================
    
    # Nombre del servicio (usado en logs y métricas)
    SERVICE_NAME: str = "auth-service"
    
    # Entorno de ejecución: development, staging, production
    ENVIRONMENT: str = Field(default="development")
    
    # Modo debug (NUNCA True en producción)
    DEBUG: bool = Field(default=True)
    
    # =========================================================================
    # CONFIGURACIÓN DE BASE DE DATOS (PostgreSQL)
    # =========================================================================
    # Formato: postgresql+asyncpg://usuario:password@host:puerto/basedatos
    
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/auth_db",
        description="URL de conexión a PostgreSQL"
    )
    
    # Pool de conexiones
    DB_POOL_SIZE: int = Field(default=5, description="Tamaño del pool de conexiones")
    DB_MAX_OVERFLOW: int = Field(default=10, description="Conexiones adicionales permitidas")
    
    # =========================================================================
    # CONFIGURACIÓN DE REDIS
    # =========================================================================
    # Usado para: refresh tokens, blacklist de tokens, rate limiting
    
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="URL de conexión a Redis"
    )
    
    # =========================================================================
    # CONFIGURACIÓN DE JWT
    # =========================================================================
    # CRÍTICO: Cambiar SECRET_KEY en producción
    
    # Clave secreta para firmar tokens (mínimo 32 caracteres)
    # Generar con: openssl rand -hex 32
    SECRET_KEY: str = Field(
        default="CAMBIAR_ESTA_CLAVE_EN_PRODUCCION_usar_openssl_rand_hex_32",
        description="Clave secreta para JWT"
    )
    
    # Algoritmo de encriptación
    JWT_ALGORITHM: str = Field(default="HS256")
    
    # Tiempo de expiración del access token (en minutos)
    # Recomendación: 15-30 minutos
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="Tiempo de vida del access token en minutos"
    )
    
    # Tiempo de expiración del refresh token (en días)
    # Recomendación: 7-30 días
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7,
        description="Tiempo de vida del refresh token en días"
    )
    
    # =========================================================================
    # CONFIGURACIÓN DE OAUTH2 (Google)
    # =========================================================================
    # Obtener credenciales en: https://console.cloud.google.com/
    
    GOOGLE_CLIENT_ID: str = Field(
        default="",
        description="Client ID de Google OAuth2"
    )
    
    GOOGLE_CLIENT_SECRET: str = Field(
        default="",
        description="Client Secret de Google OAuth2"
    )
    
    GOOGLE_REDIRECT_URI: str = Field(
        default="http://localhost:8001/auth/oauth/google/callback",
        description="URI de redirección para Google OAuth2"
    )
    
    # =========================================================================
    # CONFIGURACIÓN DE OAUTH2 (Facebook)
    # =========================================================================
    # Obtener credenciales en: https://developers.facebook.com/
    
    FACEBOOK_CLIENT_ID: str = Field(
        default="",
        description="App ID de Facebook"
    )
    
    FACEBOOK_CLIENT_SECRET: str = Field(
        default="",
        description="App Secret de Facebook"
    )
    
    FACEBOOK_REDIRECT_URI: str = Field(
        default="http://localhost:8001/auth/oauth/facebook/callback",
        description="URI de redirección para Facebook OAuth2"
    )
    
    # =========================================================================
    # CONFIGURACIÓN DE EMAIL (para verificación y reset password)
    # =========================================================================
    # TODO: Configurar servicio de email (SendGrid, AWS SES, etc.)
    
    SMTP_HOST: str = Field(default="", description="Host del servidor SMTP")
    SMTP_PORT: int = Field(default=587, description="Puerto SMTP")
    SMTP_USER: str = Field(default="", description="Usuario SMTP")
    SMTP_PASSWORD: str = Field(default="", description="Contraseña SMTP")
    EMAIL_FROM: str = Field(default="noreply@ecommerce.com", description="Email remitente")
    
    # =========================================================================
    # CONFIGURACIÓN DE SEGURIDAD
    # =========================================================================
    
    # Intentos de login permitidos antes de bloquear
    MAX_LOGIN_ATTEMPTS: int = Field(default=5)
    
    # Tiempo de bloqueo después de exceder intentos (en minutos)
    LOGIN_LOCKOUT_MINUTES: int = Field(default=15)
    
    # Rate limiting: requests por minuto
    RATE_LIMIT_PER_MINUTE: int = Field(default=60)
    
    # =========================================================================
    # CONFIGURACIÓN DE CORS
    # =========================================================================
    # Lista de orígenes permitidos separados por coma
    
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000,http://localhost:8080",
        description="Orígenes permitidos para CORS (separados por coma)"
    )
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Retorna los orígenes CORS como lista."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # =========================================================================
    # CONFIGURACIÓN DE PYDANTIC SETTINGS
    # =========================================================================
    
    class Config:
        # Archivo de variables de entorno
        env_file = ".env"
        env_file_encoding = "utf-8"
        # Sensible a mayúsculas/minúsculas
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Retorna la configuración del servicio.
    
    Usa @lru_cache para crear una única instancia (singleton).
    Esto evita leer el archivo .env múltiples veces.
    
    Uso:
        from app.config import get_settings
        settings = get_settings()
        print(settings.DATABASE_URL)
    """
    return Settings()


# Instancia global de configuración
settings = get_settings()

