"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                           SERVICIO DE USUARIOS                                ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  DESCRIPCIÓN:                                                                 ║
║  Este microservicio gestiona los perfiles de usuario del ecommerce.           ║
║  Maneja la información personal, direcciones y preferencias.                  ║
║                                                                               ║
║  RESPONSABILIDADES:                                                          ║
║  - Gestión de perfiles de usuario                                            ║
║  - CRUD de direcciones de envío/facturación                                  ║
║  - Preferencias de usuario                                                   ║
║  - Administración de usuarios (para admins)                                  ║
║                                                                               ║
║  ENDPOINTS PRINCIPALES:                                                      ║
║  - GET    /users/me              - Obtener perfil actual                     ║
║  - PUT    /users/me              - Actualizar perfil                         ║
║  - GET    /users/{id}            - Obtener usuario (admin)                   ║
║  - GET    /users                 - Listar usuarios (admin)                   ║
║  - DELETE /users/{id}            - Desactivar usuario (admin)                ║
║  - GET    /users/me/addresses    - Listar direcciones                        ║
║  - POST   /users/me/addresses    - Agregar dirección                         ║
║  - PUT    /users/me/addresses/{id} - Actualizar dirección                    ║
║  - DELETE /users/me/addresses/{id} - Eliminar dirección                      ║
║                                                                               ║
║  PUERTO POR DEFECTO: 8002                                                    ║
║                                                                               ║
║  MODELOS PRINCIPALES:                                                        ║
║  - UserProfile: Datos extendidos del usuario                                 ║
║  - Address: Direcciones de envío/facturación                                 ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

__version__ = "0.1.0"
__service__ = "users"

