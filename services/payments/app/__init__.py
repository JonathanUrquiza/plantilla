"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                           SERVICIO DE PAGOS                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  DESCRIPCIÓN:                                                                 ║
║  Este microservicio gestiona los pagos del ecommerce.                         ║
║  Integra MercadoPago y está preparado para agregar más pasarelas.             ║
║                                                                               ║
║  RESPONSABILIDADES:                                                          ║
║  - Crear preferencias de pago                                                ║
║  - Procesar webhooks de pasarelas                                            ║
║  - Verificar estado de pagos                                                 ║
║  - Procesar reembolsos                                                       ║
║  - Mantener historial de transacciones                                       ║
║                                                                               ║
║  ENDPOINTS PRINCIPALES:                                                      ║
║  - POST   /payments/create       - Crear preferencia de pago                 ║
║  - GET    /payments/{id}         - Obtener estado de pago                    ║
║  - POST   /payments/webhook      - Webhook de MercadoPago                    ║
║  - POST   /payments/{id}/refund  - Procesar reembolso                        ║
║  - GET    /payments/order/{id}   - Pagos de una orden                        ║
║                                                                               ║
║  PUERTO POR DEFECTO: 8006                                                    ║
║                                                                               ║
║  INTEGRACIÓN MERCADOPAGO:                                                    ║
║  - Checkout Pro: Redirige a página de MercadoPago                            ║
║  - Webhooks: Recibe notificaciones de pagos                                  ║
║  - SDK: mercadopago>=2.2.0                                                   ║
║                                                                               ║
║  PATRÓN ADAPTADOR:                                                           ║
║  Se usa patrón adaptador para abstraer la pasarela de pago.                  ║
║  Esto permite agregar nuevas pasarelas fácilmente:                           ║
║  - MercadoPagoGateway (implementado)                                         ║
║  - StripeGateway (futuro)                                                    ║
║  - PayPalGateway (futuro)                                                    ║
║                                                                               ║
║  WEBHOOKS:                                                                   ║
║  - Verificar firma de webhooks                                               ║
║  - Procesar de forma idempotente                                             ║
║  - Reintentar en caso de fallo                                               ║
║  - Loggear todas las transacciones                                           ║
║                                                                               ║
║  SEGURIDAD:                                                                  ║
║  - Nunca loggear datos sensibles de tarjetas                                 ║
║  - Validar montos contra la orden                                            ║
║  - Verificar firmas de webhooks                                              ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

__version__ = "0.1.0"
__service__ = "payments"

