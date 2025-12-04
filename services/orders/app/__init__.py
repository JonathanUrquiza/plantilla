"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                           SERVICIO DE ÓRDENES                                 ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  DESCRIPCIÓN:                                                                 ║
║  Este microservicio gestiona las órdenes/pedidos del ecommerce.               ║
║  Maneja la creación, estados, historial y administración de pedidos.          ║
║                                                                               ║
║  RESPONSABILIDADES:                                                          ║
║  - Crear órdenes desde el carrito                                            ║
║  - Gestionar estados de órdenes                                              ║
║  - Historial de pedidos del usuario                                          ║
║  - Generación de números de orden legibles                                   ║
║  - Cancelación y modificación de órdenes                                     ║
║  - Administración de órdenes (para admins)                                   ║
║                                                                               ║
║  ENDPOINTS PRINCIPALES:                                                      ║
║  - POST   /orders              - Crear orden desde carrito                   ║
║  - GET    /orders              - Listar órdenes del usuario                  ║
║  - GET    /orders/{id}         - Obtener detalle de orden                    ║
║  - GET    /orders/number/{num} - Obtener por número de orden                 ║
║  - PUT    /orders/{id}/status  - Actualizar estado (admin)                   ║
║  - POST   /orders/{id}/cancel  - Cancelar orden                              ║
║  - GET    /orders/admin        - Listar todas las órdenes (admin)            ║
║                                                                               ║
║  PUERTO POR DEFECTO: 8005                                                    ║
║                                                                               ║
║  ESTADOS DE ORDEN:                                                           ║
║  - pending: Esperando pago                                                   ║
║  - payment_processing: Procesando pago                                       ║
║  - paid: Pago confirmado                                                     ║
║  - preparing: En preparación                                                 ║
║  - shipped: Enviado                                                          ║
║  - delivered: Entregado                                                      ║
║  - cancelled: Cancelada                                                      ║
║  - refunded: Reembolsada                                                     ║
║                                                                               ║
║  MODELOS PRINCIPALES:                                                        ║
║  - Order: Orden/pedido                                                       ║
║  - OrderItem: Items de la orden (snapshot de productos)                      ║
║  - OrderStatusHistory: Historial de cambios de estado                        ║
║                                                                               ║
║  IMPORTANTE:                                                                 ║
║  - Guardar snapshots de productos en OrderItem                               ║
║  - Los precios en la orden son los del momento de compra                     ║
║  - Generar números de orden legibles (ej: ORD-2024-0001)                     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

__version__ = "0.1.0"
__service__ = "orders"

