"""
Routers del servicio de autenticación.

Cada router agrupa endpoints relacionados.
"""

from app.routers.auth_router import router as auth_router

__all__ = ["auth_router"]

