"""
Schemas para autenticación.

Estos schemas validan los datos de entrada/salida para todos los
endpoints de autenticación.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


# ==============================================================================
# SCHEMAS DE REGISTRO
# ==============================================================================

class UserRegister(BaseModel):
    """
    Datos requeridos para registrar un nuevo usuario.
    
    VALIDACIONES A IMPLEMENTAR:
    - Email válido (automático con EmailStr)
    - Password mínimo 8 caracteres
    - Password debe contener al menos 1 número
    - Password debe contener al menos 1 mayúscula
    """
    
    email: EmailStr = Field(
        ...,
        description="Email del usuario",
        examples=["usuario@ejemplo.com"]
    )
    
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Contraseña del usuario (mínimo 8 caracteres)",
        examples=["MiPassword123"]
    )
    
    password_confirm: str = Field(
        ...,
        description="Confirmación de contraseña",
        examples=["MiPassword123"]
    )
    
    # TODO: Implementar validación de password fuerte
    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """
        Valida que el password sea suficientemente seguro.
        
        RECOMENDACIONES:
        - Mínimo 8 caracteres (ya validado con min_length)
        - Al menos una mayúscula
        - Al menos una minúscula
        - Al menos un número
        - Opcionalmente: al menos un carácter especial
        """
        # TODO: Descomentar cuando estés listo para implementar
        # if not any(c.isupper() for c in v):
        #     raise ValueError("Password debe contener al menos una mayúscula")
        # if not any(c.islower() for c in v):
        #     raise ValueError("Password debe contener al menos una minúscula")
        # if not any(c.isdigit() for c in v):
        #     raise ValueError("Password debe contener al menos un número")
        return v
    
    # TODO: Implementar validación de passwords coincidentes
    # @model_validator(mode='after')
    # def passwords_match(self):
    #     if self.password != self.password_confirm:
    #         raise ValueError("Las contraseñas no coinciden")
    #     return self


# ==============================================================================
# SCHEMAS DE LOGIN
# ==============================================================================

class LoginRequest(BaseModel):
    """
    Datos para iniciar sesión.
    """
    
    email: EmailStr = Field(
        ...,
        description="Email del usuario",
        examples=["usuario@ejemplo.com"]
    )
    
    password: str = Field(
        ...,
        description="Contraseña del usuario",
        examples=["MiPassword123"]
    )
    
    # Opcional: recordar dispositivo para token más largo
    remember_me: bool = Field(
        default=False,
        description="Si es True, el refresh token durará más tiempo"
    )


class LoginResponse(BaseModel):
    """
    Respuesta exitosa de login.
    
    Incluye:
    - access_token: Token JWT de corta duración
    - refresh_token: Token para renovar el access_token
    - token_type: Tipo de token (siempre "bearer")
    - expires_in: Segundos hasta que expire el access_token
    - user: Datos básicos del usuario
    """
    
    access_token: str = Field(
        ...,
        description="JWT access token"
    )
    
    refresh_token: str = Field(
        ...,
        description="Token para renovar el access token"
    )
    
    token_type: str = Field(
        default="bearer",
        description="Tipo de token"
    )
    
    expires_in: int = Field(
        ...,
        description="Segundos hasta que expire el access token"
    )
    
    user: "UserResponse" = Field(
        ...,
        description="Datos del usuario autenticado"
    )


# ==============================================================================
# SCHEMAS DE TOKEN
# ==============================================================================

class Token(BaseModel):
    """
    Schema para tokens JWT.
    """
    
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """
    Datos contenidos en el JWT (payload).
    
    Estos datos se extraen del token decodificado.
    """
    
    sub: str = Field(
        ...,
        description="Subject: ID del usuario"
    )
    
    email: Optional[str] = Field(
        default=None,
        description="Email del usuario"
    )
    
    role: Optional[str] = Field(
        default=None,
        description="Rol del usuario"
    )
    
    exp: Optional[datetime] = Field(
        default=None,
        description="Fecha de expiración"
    )


class RefreshTokenRequest(BaseModel):
    """
    Solicitud para renovar el access token.
    """
    
    refresh_token: str = Field(
        ...,
        description="Refresh token obtenido en el login"
    )


# ==============================================================================
# SCHEMAS DE PASSWORD
# ==============================================================================

class PasswordResetRequest(BaseModel):
    """
    Solicitud para resetear password (paso 1: enviar email).
    """
    
    email: EmailStr = Field(
        ...,
        description="Email del usuario",
        examples=["usuario@ejemplo.com"]
    )


class PasswordResetConfirm(BaseModel):
    """
    Confirmación de reset de password (paso 2: nuevo password).
    """
    
    token: str = Field(
        ...,
        description="Token recibido por email"
    )
    
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Nueva contraseña"
    )
    
    new_password_confirm: str = Field(
        ...,
        description="Confirmación de nueva contraseña"
    )


class PasswordChange(BaseModel):
    """
    Cambio de password (usuario autenticado).
    """
    
    current_password: str = Field(
        ...,
        description="Contraseña actual"
    )
    
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Nueva contraseña"
    )
    
    new_password_confirm: str = Field(
        ...,
        description="Confirmación de nueva contraseña"
    )


# ==============================================================================
# SCHEMAS DE RESPUESTA
# ==============================================================================

class UserResponse(BaseModel):
    """
    Datos del usuario en respuestas.
    
    NO incluir datos sensibles como password.
    """
    
    id: UUID = Field(
        ...,
        description="ID único del usuario"
    )
    
    email: EmailStr = Field(
        ...,
        description="Email del usuario"
    )
    
    is_active: bool = Field(
        ...,
        description="Si el usuario está activo"
    )
    
    is_verified: bool = Field(
        ...,
        description="Si el email fue verificado"
    )
    
    role: str = Field(
        ...,
        description="Rol del usuario"
    )
    
    created_at: datetime = Field(
        ...,
        description="Fecha de creación"
    )
    
    class Config:
        from_attributes = True  # Permite crear desde objetos ORM


class MessageResponse(BaseModel):
    """
    Respuesta genérica con mensaje.
    """
    
    message: str = Field(
        ...,
        description="Mensaje de respuesta"
    )
    
    success: bool = Field(
        default=True,
        description="Si la operación fue exitosa"
    )


# ==============================================================================
# SCHEMAS DE OAUTH
# ==============================================================================

class OAuthCallback(BaseModel):
    """
    Datos recibidos en callback de OAuth.
    
    TODO: Implementar según el proveedor (Google, Facebook).
    """
    
    code: str = Field(
        ...,
        description="Código de autorización del proveedor"
    )
    
    state: Optional[str] = Field(
        default=None,
        description="Estado para prevenir CSRF"
    )


# Actualizar referencias forward
LoginResponse.model_rebuild()

