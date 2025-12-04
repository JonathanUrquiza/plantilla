"""
Servicio de gestión de tokens JWT.

Maneja la creación, validación y revocación de:
- Access tokens (corta duración)
- Refresh tokens (larga duración)
- Tokens de verificación (email, reset password)
"""

from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID
import secrets

from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

# TODO: Descomentar cuando implementes
# from app.models.user import User, RefreshToken
from app.config import settings
from app.schemas.auth import TokenData


class TokenService:
    """
    Servicio para gestión de tokens JWT.
    
    Responsabilidades:
    - Crear access tokens
    - Crear y almacenar refresh tokens
    - Validar tokens
    - Revocar tokens
    
    USO:
        service = TokenService()
        access_token = service.create_access_token(user)
        token_data = service.decode_token(access_token)
    """
    
    def __init__(self):
        """Inicializa el servicio con configuración."""
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.access_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS
    
    # =========================================================================
    # ACCESS TOKENS
    # =========================================================================
    
    def create_access_token(
        self, 
        user,  # User model
        additional_claims: dict = None
    ) -> str:
        """
        Crea un access token JWT.
        
        El access token contiene:
        - sub: ID del usuario
        - email: Email del usuario
        - role: Rol del usuario
        - exp: Fecha de expiración
        - iat: Fecha de emisión
        
        Args:
            user: Objeto usuario con id, email, role
            additional_claims: Claims adicionales opcionales
            
        Returns:
            Token JWT codificado
            
        EJEMPLO DE IMPLEMENTACIÓN:
        ```python
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value,
            "exp": datetime.utcnow() + timedelta(minutes=self.access_expire_minutes),
            "iat": datetime.utcnow(),
            "type": "access"
        }
        
        if additional_claims:
            payload.update(additional_claims)
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        ```
        """
        # TODO: Implementar
        raise NotImplementedError("Método pendiente de implementar")
    
    def decode_access_token(self, token: str) -> Optional[TokenData]:
        """
        Decodifica y valida un access token.
        
        Args:
            token: Token JWT a decodificar
            
        Returns:
            TokenData con los datos del token, o None si es inválido
            
        EJEMPLO DE IMPLEMENTACIÓN:
        ```python
        try:
            payload = jwt.decode(
                token, 
                self.secret_key, 
                algorithms=[self.algorithm]
            )
            
            # Verificar que es un access token
            if payload.get("type") != "access":
                return None
            
            return TokenData(
                sub=payload.get("sub"),
                email=payload.get("email"),
                role=payload.get("role"),
                exp=datetime.fromtimestamp(payload.get("exp"))
            )
        except JWTError:
            return None
        ```
        """
        # TODO: Implementar
        raise NotImplementedError("Método pendiente de implementar")
    
    # =========================================================================
    # REFRESH TOKENS
    # =========================================================================
    
    async def create_refresh_token(
        self, 
        user,  # User model
        db: AsyncSession,
        device_info: str = None
    ) -> str:
        """
        Crea y almacena un refresh token.
        
        El refresh token:
        - Es un string aleatorio único
        - Se almacena hasheado en BD
        - Tiene fecha de expiración
        - Puede incluir info del dispositivo
        
        Args:
            user: Usuario para el que crear el token
            db: Sesión de BD para guardar
            device_info: Información del dispositivo (User-Agent, etc.)
            
        Returns:
            Token en texto plano (solo se retorna una vez)
            
        EJEMPLO DE IMPLEMENTACIÓN:
        ```python
        # Generar token aleatorio
        token = secrets.token_urlsafe(32)
        
        # Hashear para almacenar
        token_hash = hash_token(token)  # Implementar función
        
        # Calcular expiración
        expires_at = datetime.utcnow() + timedelta(days=self.refresh_expire_days)
        
        # Crear registro
        refresh_token = RefreshToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at,
            device_info=device_info
        )
        db.add(refresh_token)
        await db.commit()
        
        return token  # Retornar token en texto plano
        ```
        """
        # TODO: Implementar
        raise NotImplementedError("Método pendiente de implementar")
    
    async def validate_refresh_token(
        self, 
        token: str, 
        db: AsyncSession
    ) -> Optional[UUID]:
        """
        Valida un refresh token y retorna el user_id.
        
        Validaciones:
        - Token existe en BD
        - No está revocado
        - No ha expirado
        
        Args:
            token: Refresh token a validar
            db: Sesión de BD
            
        Returns:
            user_id si es válido, None si no
            
        EJEMPLO DE IMPLEMENTACIÓN:
        ```python
        # Hashear token para buscar
        token_hash = hash_token(token)
        
        # Buscar en BD
        query = select(RefreshToken).where(
            RefreshToken.token_hash == token_hash,
            RefreshToken.revoked == False,
            RefreshToken.expires_at > datetime.utcnow()
        )
        result = await db.execute(query)
        refresh_token = result.scalar_one_or_none()
        
        if not refresh_token:
            return None
        
        return refresh_token.user_id
        ```
        """
        # TODO: Implementar
        raise NotImplementedError("Método pendiente de implementar")
    
    async def revoke_refresh_token(
        self, 
        token: str, 
        db: AsyncSession
    ) -> bool:
        """
        Revoca un refresh token específico.
        
        Args:
            token: Token a revocar
            db: Sesión de BD
            
        Returns:
            True si se revocó, False si no existía
            
        EJEMPLO DE IMPLEMENTACIÓN:
        ```python
        token_hash = hash_token(token)
        
        query = update(RefreshToken).where(
            RefreshToken.token_hash == token_hash
        ).values(revoked=True)
        
        result = await db.execute(query)
        await db.commit()
        
        return result.rowcount > 0
        ```
        """
        # TODO: Implementar
        raise NotImplementedError("Método pendiente de implementar")
    
    async def revoke_all_user_tokens(
        self, 
        user_id: UUID, 
        db: AsyncSession
    ) -> int:
        """
        Revoca todos los refresh tokens de un usuario.
        
        Útil para:
        - Cambio de password
        - Compromiso de cuenta
        - "Cerrar sesión en todos los dispositivos"
        
        Args:
            user_id: ID del usuario
            db: Sesión de BD
            
        Returns:
            Cantidad de tokens revocados
            
        EJEMPLO DE IMPLEMENTACIÓN:
        ```python
        query = update(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked == False
        ).values(revoked=True)
        
        result = await db.execute(query)
        await db.commit()
        
        return result.rowcount
        ```
        """
        # TODO: Implementar
        raise NotImplementedError("Método pendiente de implementar")
    
    # =========================================================================
    # TOKENS DE PROPÓSITO ESPECIAL
    # =========================================================================
    
    def create_verification_token(self, user_id: UUID) -> str:
        """
        Crea un token para verificación de email.
        
        Características:
        - Expiración corta (24 horas)
        - Incluye user_id
        - Incluye propósito "verify"
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Token JWT
        """
        # TODO: Implementar
        # payload = {
        #     "sub": str(user_id),
        #     "purpose": "verify",
        #     "exp": datetime.utcnow() + timedelta(hours=24),
        #     "iat": datetime.utcnow()
        # }
        # return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        raise NotImplementedError("Método pendiente de implementar")
    
    def create_reset_token(self, user_id: UUID) -> str:
        """
        Crea un token para reset de password.
        
        Características:
        - Expiración muy corta (1 hora)
        - Incluye user_id
        - Incluye propósito "reset"
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Token JWT
        """
        # TODO: Implementar
        # payload = {
        #     "sub": str(user_id),
        #     "purpose": "reset",
        #     "exp": datetime.utcnow() + timedelta(hours=1),
        #     "iat": datetime.utcnow()
        # }
        # return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        raise NotImplementedError("Método pendiente de implementar")
    
    def decode_special_token(
        self, 
        token: str, 
        expected_purpose: str
    ) -> Optional[UUID]:
        """
        Decodifica un token de propósito especial.
        
        Args:
            token: Token a decodificar
            expected_purpose: Propósito esperado ("verify" o "reset")
            
        Returns:
            user_id si es válido y el propósito coincide, None si no
        """
        # TODO: Implementar
        # try:
        #     payload = jwt.decode(
        #         token, 
        #         self.secret_key, 
        #         algorithms=[self.algorithm]
        #     )
        #     
        #     if payload.get("purpose") != expected_purpose:
        #         return None
        #     
        #     return UUID(payload.get("sub"))
        # except (JWTError, ValueError):
        #     return None
        raise NotImplementedError("Método pendiente de implementar")


# ==============================================================================
# FUNCIONES AUXILIARES
# ==============================================================================

def hash_token(token: str) -> str:
    """
    Hashea un token para almacenamiento seguro.
    
    NOTA: Usar un hash simple (SHA256) es suficiente para tokens
    aleatorios de alta entropía. No usar bcrypt aquí porque:
    - Los tokens son aleatorios, no elegidos por usuarios
    - Necesitamos búsquedas rápidas en BD
    
    Args:
        token: Token en texto plano
        
    Returns:
        Hash del token
    """
    import hashlib
    return hashlib.sha256(token.encode()).hexdigest()

