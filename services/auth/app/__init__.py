"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                           SERVICIO DE AUTENTICACIÓN                           ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  DESCRIPCIÓN:                                                                 ║
║  Este microservicio maneja toda la autenticación y autorización del          ║
║  sistema de ecommerce. Implementa OAuth2 con JWT para un sistema             ║
║  de tokens seguro y escalable.                                               ║
║                                                                               ║
║  RESPONSABILIDADES:                                                          ║
║  - Registro de nuevos usuarios                                               ║
║  - Login con email/password                                                  ║
║  - Login con proveedores OAuth2 (Google, Facebook)                           ║
║  - Generación y validación de JWT (access + refresh tokens)                  ║
║  - Logout e invalidación de tokens                                           ║
║  - Reset y cambio de contraseña                                              ║
║  - Verificación de email                                                     ║
║                                                                               ║
║  TECNOLOGÍAS:                                                                ║
║  - FastAPI: Framework web                                                    ║
║  - python-jose: Manejo de JWT                                                ║
║  - passlib + bcrypt: Hasheo de contraseñas                                   ║
║  - Redis: Almacenamiento de refresh tokens y blacklist                       ║
║  - PostgreSQL: Almacenamiento de credenciales                                ║
║                                                                               ║
║  ENDPOINTS PRINCIPALES:                                                      ║
║  - POST /auth/register     - Registro de usuario                             ║
║  - POST /auth/login        - Login con credenciales                          ║
║  - POST /auth/logout       - Cerrar sesión                                   ║
║  - POST /auth/refresh      - Renovar access token                            ║
║  - POST /auth/password/reset - Solicitar reset de password                   ║
║  - POST /auth/password/change - Cambiar password                             ║
║  - GET  /auth/verify/{token} - Verificar email                               ║
║  - GET  /auth/oauth/google   - Login con Google                              ║
║  - GET  /auth/oauth/facebook - Login con Facebook                            ║
║                                                                               ║
║  PUERTO POR DEFECTO: 8001                                                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

__version__ = "0.1.0"
__service__ = "auth"

