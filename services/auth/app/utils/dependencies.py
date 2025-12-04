"""
Dependencies de FastAPI para autenticación.

Estas funciones se usan con Depends() en los endpoints
para obtener el usuario actual y verificar permisos.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.config import settings

# TODO: Descomentar cuando implementes
# from app.models.user import User, UserRole
# from app.services.token_service import TokenService
# from app.schemas.auth import TokenData


# ==============================================================================
# ESQUEMA DE SEGURIDAD OAUTH2
# ==============================================================================
# Configura cómo FastAPI espera recibir el token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",  # URL donde se obtiene el token
    auto_error=True  # Lanzar error si no hay token
)

# Versión opcional (no lanza error si no hay token)
oauth2_scheme_optional = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    auto_error=False
)


# ==============================================================================
# DEPENDENCY: OBTENER USUARIO ACTUAL
# ==============================================================================

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """
    Obtiene el usuario actual desde el token JWT.
    
    Esta dependency:
    1. Extrae el token del header Authorization
    2. Decodifica y valida el JWT
    3. Obtiene el usuario de la BD
    4. Retorna el usuario
    
    USO EN ENDPOINTS:
    ```python
    @router.get("/me")
    async def get_me(current_user: User = Depends(get_current_user)):
        return current_user
    ```
    
    Args:
        token: Token JWT extraído del header
        db: Sesión de BD
        
    Returns:
        Usuario autenticado
        
    Raises:
        HTTPException 401: Si el token es inválido o expiró
        HTTPException 401: Si el usuario no existe
    """
    # Excepción estándar para credenciales inválidas
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # TODO: Implementar
    # 
    # # 1. Decodificar token
    # token_service = TokenService()
    # token_data = token_service.decode_access_token(token)
    # 
    # if token_data is None:
    #     raise credentials_exception
    # 
    # # 2. Obtener usuario de BD
    # from sqlalchemy import select
    # from app.models.user import User
    # 
    # query = select(User).where(User.id == token_data.sub)
    # result = await db.execute(query)
    # user = result.scalar_one_or_none()
    # 
    # if user is None:
    #     raise credentials_exception
    # 
    # return user
    
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Dependency pendiente de implementar"
    )


async def get_current_user_optional(
    token: str = Depends(oauth2_scheme_optional),
    db: AsyncSession = Depends(get_db)
):
    """
    Obtiene el usuario actual si hay token, o None si no.
    
    Útil para endpoints que funcionan diferente si el usuario
    está autenticado o no.
    
    USO:
    ```python
    @router.get("/products")
    async def get_products(
        current_user: Optional[User] = Depends(get_current_user_optional)
    ):
        if current_user:
            # Mostrar precios especiales
            pass
        else:
            # Mostrar precios normales
            pass
    ```
    """
    if not token:
        return None
    
    try:
        return await get_current_user(token, db)
    except HTTPException:
        return None


# ==============================================================================
# DEPENDENCY: USUARIO ACTIVO
# ==============================================================================

async def get_current_active_user(
    current_user = Depends(get_current_user)
):
    """
    Verifica que el usuario esté activo.
    
    Agrega validación adicional sobre get_current_user.
    
    Args:
        current_user: Usuario del token
        
    Returns:
        Usuario si está activo
        
    Raises:
        HTTPException 403: Si el usuario está desactivado
    """
    # TODO: Implementar
    # if not current_user.is_active:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Usuario desactivado"
    #     )
    # return current_user
    
    return current_user


async def get_current_verified_user(
    current_user = Depends(get_current_active_user)
):
    """
    Verifica que el email del usuario esté verificado.
    
    Útil para endpoints que requieren verificación.
    
    Args:
        current_user: Usuario activo
        
    Returns:
        Usuario si está verificado
        
    Raises:
        HTTPException 403: Si el email no está verificado
    """
    # TODO: Implementar
    # if not current_user.is_verified:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Email no verificado"
    #     )
    # return current_user
    
    return current_user


# ==============================================================================
# DEPENDENCY: VERIFICAR ROL
# ==============================================================================

def require_role(required_role: str):
    """
    Factory de dependency que verifica el rol del usuario.
    
    USO:
    ```python
    @router.delete("/users/{id}")
    async def delete_user(
        id: UUID,
        admin: User = Depends(require_role("admin"))
    ):
        # Solo admins pueden borrar usuarios
        pass
    ```
    
    Args:
        required_role: Rol requerido ("admin", "seller", "customer")
        
    Returns:
        Dependency function
    """
    async def role_checker(
        current_user = Depends(get_current_active_user)
    ):
        # TODO: Implementar
        # if current_user.role.value != required_role:
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail=f"Se requiere rol: {required_role}"
        #     )
        # return current_user
        return current_user
    
    return role_checker


def require_roles(allowed_roles: list[str]):
    """
    Factory de dependency que verifica múltiples roles.
    
    USO:
    ```python
    @router.get("/dashboard")
    async def dashboard(
        user: User = Depends(require_roles(["admin", "seller"]))
    ):
        # Admins y sellers pueden ver el dashboard
        pass
    ```
    
    Args:
        allowed_roles: Lista de roles permitidos
        
    Returns:
        Dependency function
    """
    async def roles_checker(
        current_user = Depends(get_current_active_user)
    ):
        # TODO: Implementar
        # if current_user.role.value not in allowed_roles:
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail=f"Se requiere uno de estos roles: {allowed_roles}"
        #     )
        # return current_user
        return current_user
    
    return roles_checker


# ==============================================================================
# DEPENDENCY: ADMIN REQUERIDO
# ==============================================================================

# Shortcut común para requerir admin
require_admin = require_role("admin")

