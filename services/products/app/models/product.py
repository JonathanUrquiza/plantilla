"""
Modelos de productos y categorías.

Este servicio maneja todo el catálogo del ecommerce.
"""

import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum as PyEnum

from sqlalchemy import (
    Column, String, Boolean, DateTime, 
    ForeignKey, Enum, Text, Integer, Numeric,
    Index
)
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
from sqlalchemy.orm import relationship

# TODO: Importar Base desde database.py
from sqlalchemy.orm import declarative_base
Base = declarative_base()


# ==============================================================================
# ENUMS
# ==============================================================================

class ProductStatus(str, PyEnum):
    """Estado del producto."""
    DRAFT = "draft"           # Borrador, no visible
    ACTIVE = "active"         # Activo y visible
    INACTIVE = "inactive"     # Inactivo temporalmente
    OUT_OF_STOCK = "out_of_stock"  # Sin stock
    DISCONTINUED = "discontinued"   # Descontinuado


class ProductType(str, PyEnum):
    """Tipo de producto."""
    PHYSICAL = "physical"     # Producto físico con envío
    DIGITAL = "digital"       # Producto digital (descarga)
    HYBRID = "hybrid"         # Físico + digital


# ==============================================================================
# MODELO: Category
# ==============================================================================

class Category(Base):
    """
    Categoría de productos.
    
    Soporta jerarquía de categorías (categoría padre/hijas).
    
    CAMPOS A IMPLEMENTAR:
    """
    __tablename__ = "categories"
    
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    # Nombre de la categoría
    name = Column(
        String(100), 
        nullable=False,
        comment="Nombre de la categoría"
    )
    
    # Slug para URLs amigables (ej: "ropa-deportiva")
    # TODO: Generar automáticamente desde name
    slug = Column(
        String(100), 
        unique=True, 
        index=True,
        nullable=False,
        comment="Slug para URL amigable"
    )
    
    # Descripción (opcional)
    description = Column(
        Text, 
        nullable=True,
        comment="Descripción de la categoría"
    )
    
    # Imagen de la categoría
    image_url = Column(
        String(500), 
        nullable=True,
        comment="URL de la imagen de la categoría"
    )
    
    # Categoría padre (para subcategorías)
    # NULL = categoría raíz
    parent_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="ID de la categoría padre (null = raíz)"
    )
    
    # Orden de visualización
    display_order = Column(
        Integer, 
        default=0,
        comment="Orden de visualización en listados"
    )
    
    # Estado
    is_active = Column(
        Boolean, 
        default=True,
        comment="Si la categoría está activa"
    )
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    parent = relationship("Category", remote_side=[id], backref="children")
    products = relationship("Product", back_populates="category")
    
    def __repr__(self):
        return f"<Category {self.name}>"


# ==============================================================================
# MODELO: Product
# ==============================================================================

class Product(Base):
    """
    Producto del catálogo.
    
    CAMPOS A IMPLEMENTAR:
    - Información básica (nombre, descripción, SKU)
    - Precios (precio, precio anterior)
    - Inventario (stock)
    - Estado y visibilidad
    - SEO (meta tags)
    - Tipo (físico/digital)
    
    IMPORTANTE: Usar Decimal para precios, nunca float
    """
    __tablename__ = "products"
    
    # =========================================================================
    # Identificación
    # =========================================================================
    
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    # SKU (Stock Keeping Unit) - código único del producto
    # TODO: Generar automáticamente o validar unicidad
    sku = Column(
        String(50), 
        unique=True, 
        index=True,
        nullable=False,
        comment="Código único del producto"
    )
    
    # Slug para URLs amigables
    slug = Column(
        String(200), 
        unique=True, 
        index=True,
        nullable=False,
        comment="Slug para URL amigable"
    )
    
    # =========================================================================
    # Información básica
    # =========================================================================
    
    # Nombre del producto
    name = Column(
        String(200), 
        nullable=False,
        index=True,
        comment="Nombre del producto"
    )
    
    # Descripción corta (para listados)
    short_description = Column(
        String(500), 
        nullable=True,
        comment="Descripción corta para listados"
    )
    
    # Descripción completa (HTML permitido)
    description = Column(
        Text, 
        nullable=True,
        comment="Descripción completa del producto"
    )
    
    # =========================================================================
    # Precios
    # =========================================================================
    # IMPORTANTE: Usar Numeric/Decimal, NO Float
    
    # Precio actual
    price = Column(
        Numeric(10, 2), 
        nullable=False,
        comment="Precio actual del producto"
    )
    
    # Precio anterior (para mostrar descuento)
    compare_price = Column(
        Numeric(10, 2), 
        nullable=True,
        comment="Precio anterior (tachado)"
    )
    
    # Costo del producto (para calcular margen)
    cost = Column(
        Numeric(10, 2), 
        nullable=True,
        comment="Costo del producto (interno)"
    )
    
    # =========================================================================
    # Inventario
    # =========================================================================
    
    # Stock disponible
    stock = Column(
        Integer, 
        default=0,
        comment="Cantidad en stock"
    )
    
    # Stock mínimo para alerta
    low_stock_threshold = Column(
        Integer, 
        default=5,
        comment="Umbral para alerta de stock bajo"
    )
    
    # Permitir venta sin stock
    allow_backorder = Column(
        Boolean, 
        default=False,
        comment="Permitir vender sin stock"
    )
    
    # =========================================================================
    # Tipo y características
    # =========================================================================
    
    # Tipo de producto
    product_type = Column(
        Enum(ProductType), 
        default=ProductType.PHYSICAL,
        comment="Tipo de producto (físico/digital/híbrido)"
    )
    
    # Si es producto digital
    is_digital = Column(
        Boolean, 
        default=False,
        comment="Si es producto digital"
    )
    
    # URL del archivo digital (si aplica)
    # TODO: Usar servicio Downloads para seguridad
    digital_file_url = Column(
        String(500), 
        nullable=True,
        comment="URL del archivo digital (si aplica)"
    )
    
    # Peso (para cálculo de envío)
    weight = Column(
        Numeric(8, 2), 
        nullable=True,
        comment="Peso en kg (para cálculo de envío)"
    )
    
    # Dimensiones (para cálculo de envío)
    length = Column(Numeric(8, 2), nullable=True, comment="Largo en cm")
    width = Column(Numeric(8, 2), nullable=True, comment="Ancho en cm")
    height = Column(Numeric(8, 2), nullable=True, comment="Alto en cm")
    
    # =========================================================================
    # Categorización
    # =========================================================================
    
    # Categoría principal
    category_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Categoría del producto"
    )
    
    # Tags (almacenados como string separado por comas)
    # TODO: Considerar tabla separada para tags
    tags = Column(
        String(500), 
        nullable=True,
        comment="Tags separados por coma"
    )
    
    # =========================================================================
    # Estado y visibilidad
    # =========================================================================
    
    # Estado del producto
    status = Column(
        Enum(ProductStatus), 
        default=ProductStatus.DRAFT,
        index=True,
        comment="Estado del producto"
    )
    
    # Producto destacado
    is_featured = Column(
        Boolean, 
        default=False,
        index=True,
        comment="Si es producto destacado"
    )
    
    # Orden de visualización
    display_order = Column(
        Integer, 
        default=0,
        comment="Orden en listados"
    )
    
    # =========================================================================
    # SEO
    # =========================================================================
    
    meta_title = Column(
        String(70), 
        nullable=True,
        comment="Título para SEO"
    )
    
    meta_description = Column(
        String(160), 
        nullable=True,
        comment="Descripción para SEO"
    )
    
    # =========================================================================
    # Búsqueda full-text (PostgreSQL)
    # =========================================================================
    # TODO: Configurar trigger para actualizar automáticamente
    
    # search_vector = Column(
    #     TSVECTOR,
    #     comment="Vector de búsqueda full-text"
    # )
    
    # =========================================================================
    # Timestamps
    # =========================================================================
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime, nullable=True, comment="Fecha de publicación")
    
    # =========================================================================
    # Relaciones
    # =========================================================================
    
    category = relationship("Category", back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")
    
    # =========================================================================
    # Índices
    # =========================================================================
    
    __table_args__ = (
        Index('idx_product_category_status', 'category_id', 'status'),
        Index('idx_product_featured', 'is_featured', 'status'),
    )
    
    # =========================================================================
    # Propiedades
    # =========================================================================
    
    @property
    def is_on_sale(self) -> bool:
        """Verifica si el producto está en oferta."""
        return self.compare_price is not None and self.compare_price > self.price
    
    @property
    def discount_percentage(self) -> int:
        """Calcula el porcentaje de descuento."""
        if not self.is_on_sale:
            return 0
        return int(((self.compare_price - self.price) / self.compare_price) * 100)
    
    @property
    def is_in_stock(self) -> bool:
        """Verifica si hay stock disponible."""
        return self.stock > 0 or self.allow_backorder
    
    @property
    def is_low_stock(self) -> bool:
        """Verifica si el stock está bajo."""
        return 0 < self.stock <= self.low_stock_threshold
    
    def __repr__(self):
        return f"<Product {self.name}>"


# ==============================================================================
# MODELO: ProductImage
# ==============================================================================

class ProductImage(Base):
    """
    Imágenes de productos.
    
    Un producto puede tener múltiples imágenes.
    """
    __tablename__ = "product_images"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    product_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # URL de la imagen
    url = Column(
        String(500), 
        nullable=False,
        comment="URL de la imagen"
    )
    
    # Texto alternativo (accesibilidad y SEO)
    alt_text = Column(
        String(200), 
        nullable=True,
        comment="Texto alternativo para la imagen"
    )
    
    # Orden de visualización
    display_order = Column(
        Integer, 
        default=0,
        comment="Orden de visualización"
    )
    
    # Si es la imagen principal
    is_primary = Column(
        Boolean, 
        default=False,
        comment="Si es la imagen principal"
    )
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relación
    product = relationship("Product", back_populates="images")
    
    def __repr__(self):
        return f"<ProductImage {self.product_id}>"


# ==============================================================================
# MODELO: ProductVariant
# ==============================================================================

class ProductVariant(Base):
    """
    Variantes de producto (talla, color, etc.).
    
    Cada variante puede tener su propio precio y stock.
    
    EJEMPLO:
    - Producto: "Camiseta"
    - Variantes: "Talla S", "Talla M", "Talla L"
    """
    __tablename__ = "product_variants"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    product_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # SKU de la variante
    sku = Column(
        String(50), 
        unique=True,
        nullable=False,
        comment="SKU de la variante"
    )
    
    # Nombre de la variante (ej: "Talla M - Rojo")
    name = Column(
        String(100), 
        nullable=False,
        comment="Nombre de la variante"
    )
    
    # Opciones (ej: {"talla": "M", "color": "Rojo"})
    # TODO: Usar JSONB para mayor flexibilidad
    option1_name = Column(String(50), nullable=True, comment="Nombre opción 1 (ej: Talla)")
    option1_value = Column(String(50), nullable=True, comment="Valor opción 1 (ej: M)")
    option2_name = Column(String(50), nullable=True, comment="Nombre opción 2 (ej: Color)")
    option2_value = Column(String(50), nullable=True, comment="Valor opción 2 (ej: Rojo)")
    option3_name = Column(String(50), nullable=True)
    option3_value = Column(String(50), nullable=True)
    
    # Precio (puede ser diferente al producto base)
    price = Column(
        Numeric(10, 2), 
        nullable=True,
        comment="Precio de la variante (null = usar precio del producto)"
    )
    
    # Stock de esta variante
    stock = Column(
        Integer, 
        default=0,
        comment="Stock de la variante"
    )
    
    # Peso (puede variar por variante)
    weight = Column(
        Numeric(8, 2), 
        nullable=True,
        comment="Peso de la variante"
    )
    
    # Imagen de la variante
    image_url = Column(
        String(500), 
        nullable=True,
        comment="Imagen específica de la variante"
    )
    
    # Estado
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación
    product = relationship("Product", back_populates="variants")
    
    def __repr__(self):
        return f"<ProductVariant {self.name}>"

