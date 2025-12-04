"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                           SERVICIO DE ENVÍOS                                  ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  DESCRIPCIÓN:                                                                 ║
║  Este microservicio gestiona los envíos y direcciones del ecommerce.          ║
║  Calcula costos de envío y maneja la integración con proveedores.             ║
║                                                                               ║
║  RESPONSABILIDADES:                                                          ║
║  - Calcular costos de envío                                                  ║
║  - Gestionar métodos de envío disponibles                                    ║
║  - Integrar con proveedores (Andreani, OCA, etc.)                            ║
║  - Generar etiquetas de envío                                                ║
║  - Rastrear envíos                                                           ║
║                                                                               ║
║  ENDPOINTS PRINCIPALES:                                                      ║
║  - POST   /shipping/calculate    - Calcular costos de envío                  ║
║  - GET    /shipping/methods      - Obtener métodos disponibles               ║
║  - GET    /shipping/track/{num}  - Rastrear envío                            ║
║  - POST   /shipping/label        - Generar etiqueta (admin)                  ║
║                                                                               ║
║  PUERTO POR DEFECTO: 8007                                                    ║
║                                                                               ║
║  MÉTODOS DE ENVÍO:                                                           ║
║  - standard: Envío estándar (5-7 días)                                       ║
║  - express: Envío express (1-3 días)                                         ║
║  - pickup: Retiro en sucursal                                                ║
║  - free: Envío gratis (según condiciones)                                    ║
║                                                                               ║
║  PROVEEDORES SOPORTADOS:                                                     ║
║  - Andreani                                                                  ║
║  - OCA                                                                       ║
║  - Correo Argentino                                                          ║
║  - Envío propio                                                              ║
║                                                                               ║
║  CÁLCULO DE COSTOS:                                                          ║
║  - Por peso                                                                  ║
║  - Por volumen                                                               ║
║  - Por zona/distancia                                                        ║
║  - Tarifas fijas                                                             ║
║  - Envío gratis a partir de X monto                                          ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

__version__ = "0.1.0"
__service__ = "shipping"

