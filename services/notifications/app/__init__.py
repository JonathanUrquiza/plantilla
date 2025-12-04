"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                           SERVICIO DE NOTIFICACIONES                          ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  DESCRIPCIÓN:                                                                 ║
║  Este microservicio gestiona todas las notificaciones del ecommerce.          ║
║  Envía emails, push notifications y otros tipos de comunicación.              ║
║                                                                               ║
║  RESPONSABILIDADES:                                                          ║
║  - Enviar emails transaccionales                                             ║
║  - Enviar push notifications (opcional)                                      ║
║  - Gestionar templates de emails                                             ║
║  - Cola de notificaciones                                                    ║
║  - Historial de notificaciones enviadas                                      ║
║                                                                               ║
║  ENDPOINTS PRINCIPALES:                                                      ║
║  - POST   /notifications/send    - Enviar notificación                       ║
║  - GET    /notifications         - Listar notificaciones del usuario         ║
║  - PUT    /notifications/{id}/read - Marcar como leída                       ║
║  - POST   /notifications/email   - Enviar email                              ║
║                                                                               ║
║  PUERTO POR DEFECTO: 8008                                                    ║
║                                                                               ║
║  TIPOS DE NOTIFICACIÓN:                                                      ║
║  - order_confirmed: Confirmación de orden                                    ║
║  - order_shipped: Orden enviada                                              ║
║  - order_delivered: Orden entregada                                          ║
║  - payment_received: Pago recibido                                           ║
║  - payment_failed: Pago fallido                                              ║
║  - password_reset: Reset de contraseña                                       ║
║  - welcome: Bienvenida a nuevo usuario                                       ║
║  - email_verification: Verificación de email                                 ║
║                                                                               ║
║  CANALES:                                                                    ║
║  - Email: SendGrid, AWS SES, o SMTP                                          ║
║  - Push: Firebase Cloud Messaging (opcional)                                 ║
║  - SMS: Twilio (opcional)                                                    ║
║                                                                               ║
║  TEMPLATES:                                                                  ║
║  - HTML con variables dinámicas                                              ║
║  - Versión texto plano como fallback                                         ║
║  - Soporte para múltiples idiomas                                            ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

__version__ = "0.1.0"
__service__ = "notifications"

