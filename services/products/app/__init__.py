"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                           SERVICIO DE PRODUCTOS                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  DESCRIPCIÓN:                                                                 ║
║  Este microservicio gestiona el catálogo de productos del ecommerce.          ║
║  Maneja productos, categorías, inventario e imágenes.                         ║
║                                                                               ║
║  RESPONSABILIDADES:                                                          ║
║  - CRUD de productos                                                         ║
║  - Gestión de categorías y subcategorías                                     ║
║  - Control de inventario (stock)                                             ║
║  - Gestión de imágenes de productos                                          ║
║  - Búsqueda y filtrado de productos                                          ║
║  - Productos destacados y ofertas                                            ║
║                                                                               ║
║  ENDPOINTS PRINCIPALES:                                                      ║
║  - GET    /products              - Listar productos (con filtros)            ║
║  - GET    /products/{id}         - Obtener producto                          ║
║  - GET    /products/slug/{slug}  - Obtener por slug                          ║
║  - POST   /products              - Crear producto (admin)                    ║
║  - PUT    /products/{id}         - Actualizar producto (admin)               ║
║  - DELETE /products/{id}         - Eliminar producto (admin)                 ║
║  - GET    /categories            - Listar categorías                         ║
║  - POST   /categories            - Crear categoría (admin)                   ║
║  - PUT    /products/{id}/stock   - Actualizar stock                          ║
║                                                                               ║
║  PUERTO POR DEFECTO: 8003                                                    ║
║                                                                               ║
║  MODELOS PRINCIPALES:                                                        ║
║  - Product: Producto del catálogo                                            ║
║  - Category: Categoría de productos                                          ║
║  - ProductImage: Imágenes de productos                                       ║
║  - ProductVariant: Variantes (talla, color, etc.)                            ║
║                                                                               ║
║  CONSIDERACIONES:                                                            ║
║  - Usar cache Redis para productos populares                                 ║
║  - Implementar búsqueda full-text con PostgreSQL                             ║
║  - Manejar productos digitales (is_digital = True)                           ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

__version__ = "0.1.0"
__service__ = "products"

