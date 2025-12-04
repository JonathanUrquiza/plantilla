"""
Modelos relacionados con usuarios y autenticación.

NOTA: Este servicio solo maneja las credenciales de autenticación.
Los datos completos del perfil se gestionan en el servicio Users.
"""

import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    Column, String, Boolean, DateTime, 
    ForeignKey, Enum, Text, Integer
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


# ==============================================================================
# ENUMS
# ==============================================================================

class AuthProvider(str, PyEnum):
    """
    Proveedores de autenticación soportados.
    
    Agregar aquí nuevos proveedores OAuth2 cuando se implementen.
    """
    LOCAL = "local"          # Email/password tradicional
    GOOGLE = "google"        # OAuth2 con Google
    FACEBOOK = "facebook"    # OAuth2 con Facebook
    # TODO: Agregar más proveedores según necesidad
    # APPLE = "apple"
    # GITHUB = "github"


class UserRole(str, PyEnum):
    """
    Roles de usuario en el sistema.
    
    CUSTOMER: Usuario normal que compra
    SELLER: Vendedor (si el marketplace lo permite)
    ADMIN: Administrador del sistema
    """
    CUSTOMER = "customer"
    SELLER = "seller"
    ADMIN = "admin"


# ==============================================================================
# MODELO: User
# ==============================================================================

class User(Base):
    """
    Modelo principal de usuario para autenticación.
    
    CAMPOS A IMPLEMENTAR:
    - id: Identificador único (UUID)
    - email: Email del usuario (único, indexado)
    - is_active: Si el usuario puede hacer login
    - is_verified: Si el email fue verificado
    - role: Rol del usuario en el sistema
    - created_at: Fecha de creación
    - updated_at: Fecha de última actualización
    
    RELACIONES:
    - credentials: Lista de credenciales (password, OAuth tokens)
    - refresh_tokens: Tokens de refresco activos
    """
    __tablename__ = "users"
    
    # =========================================================================
    # Columnas principales
    # =========================================================================
    
    # ID único del usuario (usar UUID para seguridad)
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4,
        comment="Identificador único del usuario"
    )
    
    # Email del usuario (debe ser único)
    # TODO: Implementar índice para búsquedas rápidas
    email = Column(
        String(255), 
        unique=True, 
        index=True, 
        nullable=False,
        comment="Email del usuario, usado para login"
    )
    
    # Estado del usuario
    # TODO: Implementar lógica de activación/desactivación
    is_active = Column(
        Boolean, 
        default=True,
        comment="Si el usuario puede hacer login"
    )
    
    # Verificación de email
    # TODO: Implementar flujo de verificación
    is_verified = Column(
        Boolean, 
        default=False,
        comment="Si el email fue verificado"
    )
    
    # Rol del usuario
    # TODO: Implementar sistema de permisos basado en roles
    role = Column(
        Enum(UserRole), 
        default=UserRole.CUSTOMER,
        comment="Rol del usuario en el sistema"
    )
    
    # =========================================================================
    # Timestamps
    # =========================================================================
    
    created_at = Column(
        DateTime, 
        default=datetime.utcnow,
        comment="Fecha de creación del usuario"
    )
    
    updated_at = Column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow,
        comment="Fecha de última actualización"
    )
    
    # =========================================================================
    # Campos de seguridad
    # =========================================================================
    
    # Contador de intentos fallidos de login
    # TODO: Implementar bloqueo después de X intentos
    failed_login_attempts = Column(
        Integer, 
        default=0,
        comment="Intentos fallidos de login"
    )
    
    # Fecha hasta la cual el usuario está bloqueado
    # TODO: Implementar lógica de desbloqueo automático
    locked_until = Column(
        DateTime, 
        nullable=True,
        comment="Si no es null, el usuario está bloqueado hasta esta fecha"
    )
    
    # =========================================================================
    # Relaciones
    # =========================================================================
    
    # Credenciales del usuario (password, OAuth)
    credentials = relationship(
        "UserCredential", 
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    # Refresh tokens activos
    refresh_tokens = relationship(
        "RefreshToken", 
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    # =========================================================================
    # Métodos
    # =========================================================================
    
    def __repr__(self):
        return f"<User {self.email}>"


# ==============================================================================
# MODELO: UserCredential
# ==============================================================================

class UserCredential(Base):
    """
    Credenciales de autenticación del usuario.
    
    Permite múltiples métodos de autenticación por usuario:
    - Password local hasheado
    - Token de Google
    - Token de Facebook
    
    CAMPOS A IMPLEMENTAR:
    - id: Identificador único
    - user_id: FK al usuario
    - provider: Proveedor de autenticación
    - provider_user_id: ID del usuario en el proveedor (para OAuth)
    - hashed_password: Password hasheado (solo para LOCAL)
    - access_token: Token de acceso OAuth (para proveedores externos)
    - created_at: Fecha de creación
    """
    __tablename__ = "user_credentials"
    
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    # Relación con usuario
    # TODO: Implementar constraint de unicidad (user_id, provider)
    user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID del usuario propietario"
    )
    
    # Proveedor de autenticación
    provider = Column(
        Enum(AuthProvider), 
        nullable=False,
        comment="Proveedor de autenticación (local, google, facebook)"
    )
    
    # ID del usuario en el proveedor externo (para OAuth)
    # TODO: Guardar esto cuando se implemente OAuth
    provider_user_id = Column(
        String(255), 
        nullable=True,
        comment="ID del usuario en el proveedor OAuth"
    )
    
    # Password hasheado (solo para provider=LOCAL)
    # TODO: Usar bcrypt para hashear
    hashed_password = Column(
        String(255), 
        nullable=True,
        comment="Password hasheado con bcrypt (solo para LOCAL)"
    )
    
    # Token de acceso OAuth (opcional, para refrescar datos del proveedor)
    access_token = Column(
        Text, 
        nullable=True,
        comment="Access token del proveedor OAuth"
    )
    
    created_at = Column(
        DateTime, 
        default=datetime.utcnow
    )
    
    # Relación inversa
    user = relationship("User", back_populates="credentials")
    
    def __repr__(self):
        return f"<UserCredential {self.provider} for user {self.user_id}>"


# ==============================================================================
# MODELO: RefreshToken
# ==============================================================================

class RefreshToken(Base):
    """
    Tokens de refresco para renovar access tokens.
    
    Los refresh tokens se almacenan en BD para poder:
    - Revocarlos individualmente (logout)
    - Revocar todos los tokens de un usuario
    - Implementar rotación de tokens
    
    ALTERNATIVA: Usar Redis para mejor rendimiento.
    
    CAMPOS A IMPLEMENTAR:
    - id: Identificador único
    - user_id: FK al usuario
    - token: El token de refresco (hasheado)
    - expires_at: Fecha de expiración
    - created_at: Fecha de creación
    - revoked: Si el token fue revocado
    - device_info: Información del dispositivo (opcional)
    """
    __tablename__ = "refresh_tokens"
    
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Usuario propietario del token"
    )
    
    # Token hasheado (nunca guardar el token en texto plano)
    # TODO: Hashear el token antes de guardar
    token_hash = Column(
        String(255), 
        unique=True, 
        nullable=False,
        comment="Hash del refresh token"
    )
    
    # Fecha de expiración
    # TODO: Configurar según settings.REFRESH_TOKEN_EXPIRE_DAYS
    expires_at = Column(
        DateTime, 
        nullable=False,
        comment="Fecha de expiración del token"
    )
    
    created_at = Column(
        DateTime, 
        default=datetime.utcnow
    )
    
    # Si el token fue revocado (logout)
    revoked = Column(
        Boolean, 
        default=False,
        comment="Si el token fue revocado manualmente"
    )
    
    # Información del dispositivo (opcional, para "cerrar sesión en otros dispositivos")
    # TODO: Capturar User-Agent y/o device fingerprint
    device_info = Column(
        String(500), 
        nullable=True,
        comment="Información del dispositivo (User-Agent, IP, etc.)"
    )
    
    # Relación inversa
    user = relationship("User", back_populates="refresh_tokens")
    
    def __repr__(self):
        return f"<RefreshToken for user {self.user_id}>"
    
    @property
    def is_valid(self) -> bool:
        """
        Verifica si el token es válido.
        
        Un token es válido si:
        - No está revocado
        - No ha expirado
        """
        if self.revoked:
            return False
        if datetime.utcnow() > self.expires_at:
            return False
        return True

