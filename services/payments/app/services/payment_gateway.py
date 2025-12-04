"""
Interfaz y adaptadores para pasarelas de pago.

Usa el patrón Adaptador para abstraer diferentes pasarelas de pago.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID


# ==============================================================================
# ENUMS Y DATACLASSES
# ==============================================================================

class PaymentStatus(str, Enum):
    """Estado del pago."""
    PENDING = "pending"           # Esperando
    PROCESSING = "processing"     # Procesando
    APPROVED = "approved"         # Aprobado
    REJECTED = "rejected"         # Rechazado
    CANCELLED = "cancelled"       # Cancelado
    REFUNDED = "refunded"         # Reembolsado
    CHARGED_BACK = "charged_back" # Contracargo


@dataclass
class PaymentIntent:
    """
    Intención de pago (resultado de crear pago).
    
    Contiene la información necesaria para que el usuario
    complete el pago (URL de redirección, etc.).
    """
    id: str                         # ID interno del pago
    external_id: str                # ID en la pasarela
    status: PaymentStatus
    checkout_url: Optional[str]     # URL para completar pago
    qr_code: Optional[str]          # Código QR (si aplica)
    expires_at: Optional[str]       # Fecha de expiración


@dataclass
class PaymentResult:
    """
    Resultado de verificación de pago.
    """
    id: str
    external_id: str
    status: PaymentStatus
    amount: Decimal
    currency: str
    payment_method: Optional[str]
    paid_at: Optional[str]
    raw_data: dict                  # Datos originales de la pasarela


@dataclass
class RefundResult:
    """
    Resultado de un reembolso.
    """
    id: str
    payment_id: str
    status: PaymentStatus
    amount: Decimal
    reason: Optional[str]


# ==============================================================================
# INTERFAZ ABSTRACTA
# ==============================================================================

class PaymentGateway(ABC):
    """
    Interfaz abstracta para pasarelas de pago.
    
    Todas las pasarelas deben implementar estos métodos.
    Esto permite cambiar de pasarela sin modificar el resto del código.
    
    USO:
        gateway = MercadoPagoGateway()
        intent = await gateway.create_payment(order)
        # Redirigir usuario a intent.checkout_url
    """
    
    @abstractmethod
    async def create_payment(
        self,
        order_id: str,
        amount: Decimal,
        currency: str,
        description: str,
        customer_email: str,
        success_url: str,
        failure_url: str,
        pending_url: str,
        items: list[dict] = None
    ) -> PaymentIntent:
        """
        Crea una intención de pago.
        
        Args:
            order_id: ID de la orden
            amount: Monto total
            currency: Código de moneda (ARS, USD, etc.)
            description: Descripción del pago
            customer_email: Email del cliente
            success_url: URL de redirección si el pago es exitoso
            failure_url: URL de redirección si el pago falla
            pending_url: URL de redirección si el pago queda pendiente
            items: Lista de items (para mostrar en checkout)
            
        Returns:
            PaymentIntent con URL de checkout
        """
        pass
    
    @abstractmethod
    async def get_payment(self, payment_id: str) -> PaymentResult:
        """
        Obtiene el estado actual de un pago.
        
        Args:
            payment_id: ID del pago (externo)
            
        Returns:
            PaymentResult con estado actual
        """
        pass
    
    @abstractmethod
    async def verify_webhook(self, payload: dict, signature: str) -> bool:
        """
        Verifica la firma de un webhook.
        
        Args:
            payload: Datos del webhook
            signature: Firma a verificar
            
        Returns:
            True si la firma es válida
        """
        pass
    
    @abstractmethod
    async def process_webhook(self, payload: dict) -> PaymentResult:
        """
        Procesa un webhook de la pasarela.
        
        Args:
            payload: Datos del webhook
            
        Returns:
            PaymentResult con estado actualizado
        """
        pass
    
    @abstractmethod
    async def refund(
        self,
        payment_id: str,
        amount: Optional[Decimal] = None,
        reason: Optional[str] = None
    ) -> RefundResult:
        """
        Procesa un reembolso.
        
        Args:
            payment_id: ID del pago a reembolsar
            amount: Monto a reembolsar (None = total)
            reason: Razón del reembolso
            
        Returns:
            RefundResult con estado del reembolso
        """
        pass


# ==============================================================================
# IMPLEMENTACIÓN: MERCADOPAGO
# ==============================================================================

class MercadoPagoGateway(PaymentGateway):
    """
    Implementación de PaymentGateway para MercadoPago.
    
    Usa MercadoPago Checkout Pro.
    
    CONFIGURACIÓN NECESARIA:
    - MERCADOPAGO_ACCESS_TOKEN: Token de acceso
    - MERCADOPAGO_PUBLIC_KEY: Clave pública
    
    DOCUMENTACIÓN:
    https://www.mercadopago.com.ar/developers/es/docs/checkout-pro/landing
    """
    
    def __init__(self, access_token: str = None):
        """
        Inicializa el gateway con credenciales.
        
        Args:
            access_token: Token de acceso de MercadoPago.
                         Si no se proporciona, se lee de settings.
        """
        # TODO: Importar SDK de MercadoPago
        # import mercadopago
        # 
        # if access_token is None:
        #     from app.config import settings
        #     access_token = settings.MERCADOPAGO_ACCESS_TOKEN
        # 
        # self.sdk = mercadopago.SDK(access_token)
        
        self.access_token = access_token
    
    async def create_payment(
        self,
        order_id: str,
        amount: Decimal,
        currency: str,
        description: str,
        customer_email: str,
        success_url: str,
        failure_url: str,
        pending_url: str,
        items: list[dict] = None
    ) -> PaymentIntent:
        """
        Crea una preferencia de pago en MercadoPago.
        
        IMPLEMENTACIÓN:
        1. Crear objeto de preferencia
        2. Configurar items
        3. Configurar URLs de redirección
        4. Configurar datos del pagador
        5. Enviar a MercadoPago
        6. Retornar URL de checkout
        
        EJEMPLO DE IMPLEMENTACIÓN:
        ```python
        preference_data = {
            "items": [
                {
                    "title": description,
                    "quantity": 1,
                    "unit_price": float(amount),
                    "currency_id": currency
                }
            ],
            "payer": {
                "email": customer_email
            },
            "back_urls": {
                "success": success_url,
                "failure": failure_url,
                "pending": pending_url
            },
            "auto_return": "approved",
            "external_reference": order_id,
            "notification_url": "https://tu-dominio.com/payments/webhook"
        }
        
        # Si hay items detallados
        if items:
            preference_data["items"] = [
                {
                    "id": item["id"],
                    "title": item["name"],
                    "quantity": item["quantity"],
                    "unit_price": float(item["price"]),
                    "currency_id": currency
                }
                for item in items
            ]
        
        result = self.sdk.preference().create(preference_data)
        
        if result["status"] == 201:
            response = result["response"]
            return PaymentIntent(
                id=order_id,
                external_id=response["id"],
                status=PaymentStatus.PENDING,
                checkout_url=response["init_point"],
                qr_code=None,
                expires_at=response.get("expiration_date_to")
            )
        else:
            raise PaymentError(f"Error creando pago: {result}")
        ```
        """
        # TODO: Implementar con SDK de MercadoPago
        raise NotImplementedError("Método pendiente de implementar")
    
    async def get_payment(self, payment_id: str) -> PaymentResult:
        """
        Obtiene información de un pago.
        
        EJEMPLO DE IMPLEMENTACIÓN:
        ```python
        result = self.sdk.payment().get(payment_id)
        
        if result["status"] == 200:
            data = result["response"]
            
            # Mapear estado de MercadoPago a nuestro enum
            status_map = {
                "approved": PaymentStatus.APPROVED,
                "pending": PaymentStatus.PENDING,
                "in_process": PaymentStatus.PROCESSING,
                "rejected": PaymentStatus.REJECTED,
                "cancelled": PaymentStatus.CANCELLED,
                "refunded": PaymentStatus.REFUNDED,
                "charged_back": PaymentStatus.CHARGED_BACK
            }
            
            return PaymentResult(
                id=data["external_reference"],
                external_id=str(data["id"]),
                status=status_map.get(data["status"], PaymentStatus.PENDING),
                amount=Decimal(str(data["transaction_amount"])),
                currency=data["currency_id"],
                payment_method=data.get("payment_type_id"),
                paid_at=data.get("date_approved"),
                raw_data=data
            )
        ```
        """
        # TODO: Implementar
        raise NotImplementedError("Método pendiente de implementar")
    
    async def verify_webhook(self, payload: dict, signature: str) -> bool:
        """
        Verifica la firma del webhook de MercadoPago.
        
        MercadoPago envía una firma HMAC-SHA256 en el header
        x-signature que debe verificarse.
        
        TODO: Implementar verificación de firma
        """
        # TODO: Implementar
        # Ver: https://www.mercadopago.com.ar/developers/es/docs/your-integrations/notifications/webhooks
        return True  # TEMPORAL: Siempre válido (CAMBIAR EN PRODUCCIÓN)
    
    async def process_webhook(self, payload: dict) -> PaymentResult:
        """
        Procesa un webhook de MercadoPago.
        
        Tipos de notificación:
        - payment: Notificación de pago
        - merchant_order: Notificación de orden
        
        EJEMPLO DE IMPLEMENTACIÓN:
        ```python
        notification_type = payload.get("type")
        
        if notification_type == "payment":
            payment_id = payload["data"]["id"]
            return await self.get_payment(payment_id)
        
        elif notification_type == "merchant_order":
            # Procesar orden
            pass
        ```
        """
        # TODO: Implementar
        raise NotImplementedError("Método pendiente de implementar")
    
    async def refund(
        self,
        payment_id: str,
        amount: Optional[Decimal] = None,
        reason: Optional[str] = None
    ) -> RefundResult:
        """
        Procesa un reembolso en MercadoPago.
        
        EJEMPLO DE IMPLEMENTACIÓN:
        ```python
        refund_data = {}
        if amount is not None:
            refund_data["amount"] = float(amount)
        
        result = self.sdk.refund().create(payment_id, refund_data)
        
        if result["status"] in [200, 201]:
            data = result["response"]
            return RefundResult(
                id=str(data["id"]),
                payment_id=payment_id,
                status=PaymentStatus.REFUNDED,
                amount=Decimal(str(data["amount"])),
                reason=reason
            )
        ```
        """
        # TODO: Implementar
        raise NotImplementedError("Método pendiente de implementar")


# ==============================================================================
# FACTORY
# ==============================================================================

def get_payment_gateway(gateway_name: str = "mercadopago") -> PaymentGateway:
    """
    Factory para obtener la pasarela de pago.
    
    Permite cambiar de pasarela fácilmente.
    
    Args:
        gateway_name: Nombre de la pasarela
        
    Returns:
        Instancia de la pasarela
        
    Ejemplo:
        gateway = get_payment_gateway("mercadopago")
        intent = await gateway.create_payment(...)
    """
    gateways = {
        "mercadopago": MercadoPagoGateway,
        # TODO: Agregar más pasarelas
        # "stripe": StripeGateway,
        # "paypal": PayPalGateway,
    }
    
    gateway_class = gateways.get(gateway_name)
    if gateway_class is None:
        raise ValueError(f"Pasarela de pago no soportada: {gateway_name}")
    
    return gateway_class()

