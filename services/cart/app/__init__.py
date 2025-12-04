"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                           SERVICIO DE CARRITO                                 ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  DESCRIPCIÓN:                                                                 ║
║  Este microservicio gestiona los carritos de compra del ecommerce.            ║
║  Utiliza Redis para almacenamiento eficiente y rápido.                        ║
║                                                                               ║
║  RESPONSABILIDADES:                                                          ║
║  - Agregar productos al carrito                                              ║
║  - Actualizar cantidades                                                     ║
║  - Eliminar productos del carrito                                            ║
║  - Obtener contenido del carrito                                             ║
║  - Vaciar carrito                                                            ║
║  - Merge de carritos (anónimo → autenticado)                                 ║
║  - Validar stock al agregar                                                  ║
║                                                                               ║
║  ENDPOINTS PRINCIPALES:                                                      ║
║  - GET    /cart                  - Obtener carrito                           ║
║  - POST   /cart/items            - Agregar producto                          ║
║  - PUT    /cart/items/{id}       - Actualizar cantidad                       ║
║  - DELETE /cart/items/{id}       - Eliminar producto                         ║
║  - DELETE /cart                  - Vaciar carrito                            ║
║  - POST   /cart/merge            - Merge de carritos                         ║
║  - GET    /cart/count            - Obtener cantidad de items                 ║
║                                                                               ║
║  PUERTO POR DEFECTO: 8004                                                    ║
║                                                                               ║
║  ALMACENAMIENTO EN REDIS:                                                    ║
║  - Key: cart:{user_id} o cart:{session_id}                                   ║
║  - TTL: 7-30 días                                                            ║
║  - Estructura: Hash con productos                                            ║
║                                                                               ║
║  EJEMPLO DE ESTRUCTURA EN REDIS:                                             ║
║  cart:user_123 -> {                                                          ║
║      "product_abc": {"quantity": 2, "price": 100, "added_at": "..."},        ║
║      "product_xyz": {"quantity": 1, "price": 50, "added_at": "..."}          ║
║  }                                                                           ║
║                                                                               ║
║  CONSIDERACIONES:                                                            ║
║  - Carritos para usuarios anónimos (session_id)                              ║
║  - Merge de carrito al hacer login                                           ║
║  - Validar stock antes de agregar                                            ║
║  - Recalcular precios al hacer checkout (pueden cambiar)                     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

__version__ = "0.1.0"
__service__ = "cart"

