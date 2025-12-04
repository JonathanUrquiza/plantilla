"""
Modelos de órdenes y pedidos.

Las órdenes representan compras completadas o en proceso.
"""

import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum as PyEnum

from sqlalchemy import (
    Column, String, Boolean, DateTime, 
    ForeignKey, Enum, Text, Integer, Numeric
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

# TODO: Importar Base desde database.py
from sqlalchemy.orm import declarative_base
Base = declarative_base()


# ==============================================================================
# ENUMS
# ==============================================================================

class OrderStatus(str, PyEnum):
    """
    Estados posibles de una orden.
    
    FLUJO TÍPICO:
    PENDING → PAYMENT_PROCESSING → PAID → PREPARING → SHIPPED → DELIVERED
    
    FLUJOS ALTERNATIVOS:
    - PENDING → CANCELLED (usuario cancela)
    - PAID → REFUNDED (reembolso)
    """
    PENDING = "pending"                     # Creada, esperando pago
    PAYMENT_PROCESSING = "payment_processing"  # Procesando pago
    PAID = "paid"                           # Pago confirmado
    PREPARING = "preparing"                 # En preparación
    SHIPPED = "shipped"                     # Enviado
    DELIVERED = "delivered"                 # Entregado
    CANCELLED = "cancelled"                 # Cancelada
    REFUNDED = "refunded"                   # Reembolsada


class PaymentMethod(str, PyEnum):
    """Métodos de pago soportados."""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    MERCADOPAGO = "mercadopago"
    BANK_TRANSFER = "bank_transfer"
    CASH_ON_DELIVERY = "cash_on_delivery"


# ==============================================================================
# MODELO: Order
# ==============================================================================

class Order(Base):
    """
    Orden de compra.
    
    Representa una transacción completa con sus items,
    montos, dirección de envío, etc.
    
    CAMPOS A IMPLEMENTAR:
    """
    __tablename__ = "orders"
    
    # =========================================================================
    # Identificación
    # =========================================================================
    
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    # Número de orden legible (ej: ORD-2024-0001)
    # TODO: Generar automáticamente con secuencia
    order_number = Column(
        String(20), 
        unique=True, 
        index=True,
        nullable=False,
        comment="Número de orden legible"
    )
    
    # Usuario que hizo la compra
    user_id = Column(
        UUID(as_uuid=True), 
        index=True,
        nullable=False,
        comment="ID del usuario que realizó la orden"
    )
    
    # =========================================================================
    # Estado
    # =========================================================================
    
    status = Column(
        Enum(OrderStatus), 
        default=OrderStatus.PENDING,
        index=True,
        nullable=False,
        comment="Estado actual de la orden"
    )
    
    # =========================================================================
    # Montos
    # =========================================================================
    # IMPORTANTE: Usar Numeric para evitar errores de precisión
    
    # Subtotal (suma de items)
    subtotal = Column(
        Numeric(10, 2), 
        nullable=False,
        comment="Subtotal (suma de items sin descuentos)"
    )
    
    # Descuento aplicado
    discount_amount = Column(
        Numeric(10, 2), 
        default=0,
        comment="Monto de descuento aplicado"
    )
    
    # Código de cupón usado (referencia)
    coupon_code = Column(
        String(50), 
        nullable=True,
        comment="Código de cupón aplicado"
    )
    
    # Costo de envío
    shipping_cost = Column(
        Numeric(10, 2), 
        default=0,
        comment="Costo de envío"
    )
    
    # Impuestos
    tax_amount = Column(
        Numeric(10, 2), 
        default=0,
        comment="Monto de impuestos"
    )
    
    # Total final
    total = Column(
        Numeric(10, 2), 
        nullable=False,
        comment="Total a pagar (subtotal - descuento + envío + impuestos)"
    )
    
    # Moneda
    currency = Column(
        String(3), 
        default="ARS",
        comment="Código de moneda (ISO 4217)"
    )
    
    # =========================================================================
    # Pago
    # =========================================================================
    
    # Método de pago
    payment_method = Column(
        Enum(PaymentMethod), 
        nullable=True,
        comment="Método de pago utilizado"
    )
    
    # ID de pago externo (MercadoPago, etc.)
    payment_id = Column(
        String(100), 
        nullable=True,
        comment="ID de pago del proveedor"
    )
    
    # Fecha de pago
    paid_at = Column(
        DateTime, 
        nullable=True,
        comment="Fecha en que se confirmó el pago"
    )
    
    # =========================================================================
    # Dirección de envío (snapshot)
    # =========================================================================
    # Guardar copia porque la dirección del usuario puede cambiar
    
    shipping_address_id = Column(
        UUID(as_uuid=True), 
        nullable=True,
        comment="ID de la dirección (referencia)"
    )
    
    # Snapshot de la dirección
    shipping_recipient = Column(String(200), nullable=True)
    shipping_street = Column(String(200), nullable=True)
    shipping_number = Column(String(20), nullable=True)
    shipping_apartment = Column(String(50), nullable=True)
    shipping_city = Column(String(100), nullable=True)
    shipping_state = Column(String(100), nullable=True)
    shipping_postal_code = Column(String(20), nullable=True)
    shipping_country = Column(String(100), nullable=True)
    shipping_phone = Column(String(20), nullable=True)
    
    # =========================================================================
    # Dirección de facturación (snapshot)
    # =========================================================================
    
    billing_address_id = Column(UUID(as_uuid=True), nullable=True)
    billing_name = Column(String(200), nullable=True)
    billing_tax_id = Column(String(20), nullable=True, comment="CUIT/CUIL")
    
    # =========================================================================
    # Envío
    # =========================================================================
    
    # Método de envío seleccionado
    shipping_method = Column(
        String(50), 
        nullable=True,
        comment="Método de envío (ej: 'standard', 'express')"
    )
    
    # Número de seguimiento
    tracking_number = Column(
        String(100), 
        nullable=True,
        comment="Número de seguimiento del envío"
    )
    
    # URL de seguimiento
    tracking_url = Column(
        String(500), 
        nullable=True,
        comment="URL para rastrear el envío"
    )
    
    # Fecha estimada de entrega
    estimated_delivery = Column(
        DateTime, 
        nullable=True,
        comment="Fecha estimada de entrega"
    )
    
    # Fecha real de envío
    shipped_at = Column(DateTime, nullable=True)
    
    # Fecha real de entrega
    delivered_at = Column(DateTime, nullable=True)
    
    # =========================================================================
    # Notas
    # =========================================================================
    
    # Notas del cliente
    customer_notes = Column(
        Text, 
        nullable=True,
        comment="Notas del cliente al hacer el pedido"
    )
    
    # Notas internas (admin)
    internal_notes = Column(
        Text, 
        nullable=True,
        comment="Notas internas (solo visible para admins)"
    )
    
    # =========================================================================
    # Información del cliente (snapshot)
    # =========================================================================
    
    customer_email = Column(
        String(255), 
        nullable=False,
        comment="Email del cliente al momento de la compra"
    )
    
    customer_name = Column(
        String(200), 
        nullable=True,
        comment="Nombre del cliente"
    )
    
    # =========================================================================
    # Productos digitales
    # =========================================================================
    
    # Si la orden incluye productos digitales
    has_digital_items = Column(
        Boolean, 
        default=False,
        comment="Si incluye productos digitales"
    )
    
    # =========================================================================
    # Timestamps
    # =========================================================================
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cancelled_at = Column(DateTime, nullable=True)
    
    # =========================================================================
    # Relaciones
    # =========================================================================
    
    items = relationship(
        "OrderItem", 
        back_populates="order",
        cascade="all, delete-orphan"
    )
    
    status_history = relationship(
        "OrderStatusHistory", 
        back_populates="order",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Order {self.order_number}>"


# ==============================================================================
# MODELO: OrderItem
# ==============================================================================

class OrderItem(Base):
    """
    Item de una orden.
    
    Contiene snapshot del producto al momento de la compra.
    
    IMPORTANTE: Los datos del producto se copian aquí porque
    el producto original puede cambiar (precio, nombre, etc.)
    pero la orden debe mantener los datos originales.
    """
    __tablename__ = "order_items"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    order_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # =========================================================================
    # Referencia al producto
    # =========================================================================
    
    product_id = Column(
        UUID(as_uuid=True), 
        nullable=False,
        comment="ID del producto (referencia)"
    )
    
    variant_id = Column(
        UUID(as_uuid=True), 
        nullable=True,
        comment="ID de la variante (si aplica)"
    )
    
    # =========================================================================
    # Snapshot del producto
    # =========================================================================
    # Estos datos NO cambian aunque el producto se modifique
    
    product_name = Column(
        String(200), 
        nullable=False,
        comment="Nombre del producto al momento de compra"
    )
    
    product_sku = Column(
        String(50), 
        nullable=False,
        comment="SKU del producto"
    )
    
    variant_name = Column(
        String(100), 
        nullable=True,
        comment="Nombre de la variante (ej: 'Talla M - Azul')"
    )
    
    product_image = Column(
        String(500), 
        nullable=True,
        comment="URL de imagen del producto"
    )
    
    # =========================================================================
    # Cantidades y precios
    # =========================================================================
    
    quantity = Column(
        Integer, 
        nullable=False,
        comment="Cantidad comprada"
    )
    
    unit_price = Column(
        Numeric(10, 2), 
        nullable=False,
        comment="Precio unitario al momento de compra"
    )
    
    # Descuento por item (si aplica)
    discount = Column(
        Numeric(10, 2), 
        default=0,
        comment="Descuento aplicado al item"
    )
    
    # Total del item
    total = Column(
        Numeric(10, 2), 
        nullable=False,
        comment="Total (quantity * unit_price - discount)"
    )
    
    # =========================================================================
    # Información adicional
    # =========================================================================
    
    # Si es producto digital
    is_digital = Column(
        Boolean, 
        default=False,
        comment="Si es producto digital"
    )
    
    # URL de descarga (para productos digitales)
    # TODO: Usar servicio Downloads para generar URLs seguras
    download_url = Column(
        String(500), 
        nullable=True,
        comment="URL de descarga (productos digitales)"
    )
    
    # Contador de descargas
    download_count = Column(
        Integer, 
        default=0,
        comment="Veces que se descargó"
    )
    
    # Peso del item (para cálculo de envío)
    weight = Column(
        Numeric(8, 2), 
        nullable=True,
        comment="Peso del item"
    )
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relación
    order = relationship("Order", back_populates="items")
    
    def __repr__(self):
        return f"<OrderItem {self.product_name}>"


# ==============================================================================
# MODELO: OrderStatusHistory
# ==============================================================================

class OrderStatusHistory(Base):
    """
    Historial de cambios de estado de una orden.
    
    Guarda cada cambio de estado para trazabilidad.
    """
    __tablename__ = "order_status_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    order_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Estado anterior
    previous_status = Column(
        Enum(OrderStatus), 
        nullable=True,
        comment="Estado anterior (null si es el primero)"
    )
    
    # Nuevo estado
    new_status = Column(
        Enum(OrderStatus), 
        nullable=False,
        comment="Nuevo estado"
    )
    
    # Quién hizo el cambio
    changed_by = Column(
        UUID(as_uuid=True), 
        nullable=True,
        comment="ID del usuario que cambió el estado"
    )
    
    # Razón del cambio (opcional)
    reason = Column(
        String(500), 
        nullable=True,
        comment="Razón del cambio de estado"
    )
    
    # Notas adicionales
    notes = Column(
        Text, 
        nullable=True,
        comment="Notas adicionales"
    )
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relación
    order = relationship("Order", back_populates="status_history")
    
    def __repr__(self):
        return f"<OrderStatusHistory {self.previous_status} → {self.new_status}>"

