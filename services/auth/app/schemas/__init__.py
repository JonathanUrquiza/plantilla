"""
Schemas Pydantic para validación de datos.

Los schemas definen la estructura de los datos de entrada y salida
de la API, proporcionando validación automática.
"""

from app.schemas.auth import (
    # Registro
    UserRegister,
    # Login
    LoginRequest,
    LoginResponse,
    # Tokens
    Token,
    TokenData,
    RefreshTokenRequest,
    # Password
    PasswordResetRequest,
    PasswordResetConfirm,
    PasswordChange,
    # Respuestas
    UserResponse,
    MessageResponse,
)

__all__ = [
    "UserRegister",
    "LoginRequest",
    "LoginResponse",
    "Token",
    "TokenData",
    "RefreshTokenRequest",
    "PasswordResetRequest",
    "PasswordResetConfirm",
    "PasswordChange",
    "UserResponse",
    "MessageResponse",
]

