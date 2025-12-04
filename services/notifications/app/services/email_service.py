"""
Servicio de envío de emails.

Gestiona el envío de emails transaccionales usando diferentes proveedores.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List

from app.config import settings


# ==============================================================================
# ENUMS Y DATACLASSES
# ==============================================================================

class NotificationType(str, Enum):
    """Tipos de notificación."""
    ORDER_CONFIRMED = "order_confirmed"
    ORDER_SHIPPED = "order_shipped"
    ORDER_DELIVERED = "order_delivered"
    PAYMENT_RECEIVED = "payment_received"
    PAYMENT_FAILED = "payment_failed"
    PASSWORD_RESET = "password_reset"
    EMAIL_VERIFICATION = "email_verification"
    WELCOME = "welcome"
    DOWNLOAD_READY = "download_ready"


@dataclass
class EmailMessage:
    """
    Mensaje de email.
    
    Contiene toda la información necesaria para enviar un email.
    """
    to: str                         # Destinatario
    subject: str                    # Asunto
    html_content: str               # Contenido HTML
    text_content: Optional[str]     # Contenido texto (fallback)
    from_email: Optional[str]       # Remitente (usa default si no se especifica)
    from_name: Optional[str]        # Nombre del remitente
    reply_to: Optional[str]         # Email de respuesta
    cc: Optional[List[str]]         # Copia
    bcc: Optional[List[str]]        # Copia oculta
    attachments: Optional[List[dict]]  # Archivos adjuntos


@dataclass
class EmailResult:
    """Resultado del envío de email."""
    success: bool
    message_id: Optional[str]
    error: Optional[str]


# ==============================================================================
# INTERFAZ ABSTRACTA
# ==============================================================================

class EmailProvider(ABC):
    """
    Interfaz abstracta para proveedores de email.
    
    Permite cambiar de proveedor sin modificar el resto del código.
    """
    
    @abstractmethod
    async def send(self, message: EmailMessage) -> EmailResult:
        """
        Envía un email.
        
        Args:
            message: Mensaje a enviar
            
        Returns:
            Resultado del envío
        """
        pass


# ==============================================================================
# IMPLEMENTACIÓN: SMTP
# ==============================================================================

class SMTPProvider(EmailProvider):
    """
    Proveedor de email usando SMTP directo.
    
    Útil para desarrollo o servidores SMTP propios.
    """
    
    def __init__(
        self,
        host: str = None,
        port: int = None,
        username: str = None,
        password: str = None
    ):
        """
        Inicializa el proveedor SMTP.
        
        Si no se proporcionan credenciales, se leen de settings.
        """
        # TODO: Implementar
        # self.host = host or settings.SMTP_HOST
        # self.port = port or settings.SMTP_PORT
        # self.username = username or settings.SMTP_USER
        # self.password = password or settings.SMTP_PASSWORD
        pass
    
    async def send(self, message: EmailMessage) -> EmailResult:
        """
        Envía email usando SMTP.
        
        IMPLEMENTACIÓN:
        ```python
        import aiosmtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = message.subject
        msg["From"] = message.from_email or settings.EMAIL_FROM
        msg["To"] = message.to
        
        if message.text_content:
            msg.attach(MIMEText(message.text_content, "plain"))
        msg.attach(MIMEText(message.html_content, "html"))
        
        try:
            await aiosmtplib.send(
                msg,
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                use_tls=True
            )
            return EmailResult(success=True, message_id=None, error=None)
        except Exception as e:
            return EmailResult(success=False, message_id=None, error=str(e))
        ```
        """
        # TODO: Implementar
        raise NotImplementedError("Método pendiente de implementar")


# ==============================================================================
# SERVICIO DE EMAIL
# ==============================================================================

class EmailService:
    """
    Servicio principal de emails.
    
    Gestiona templates y envío de emails.
    
    USO:
        service = EmailService()
        await service.send_order_confirmation(order)
    """
    
    def __init__(self, provider: EmailProvider = None):
        """
        Inicializa el servicio.
        
        Args:
            provider: Proveedor de email (usa SMTP por defecto)
        """
        self.provider = provider or SMTPProvider()
    
    # =========================================================================
    # TEMPLATES DE EMAIL
    # =========================================================================
    
    def _render_template(
        self, 
        template_name: str, 
        context: dict
    ) -> tuple[str, str]:
        """
        Renderiza un template de email.
        
        Args:
            template_name: Nombre del template
            context: Variables para el template
            
        Returns:
            Tupla (html_content, text_content)
            
        TODO: Implementar con Jinja2 o similar
        """
        # TODO: Implementar renderizado de templates
        # 
        # from jinja2 import Environment, FileSystemLoader
        # 
        # env = Environment(loader=FileSystemLoader("templates/emails"))
        # 
        # html_template = env.get_template(f"{template_name}.html")
        # text_template = env.get_template(f"{template_name}.txt")
        # 
        # return (
        #     html_template.render(**context),
        #     text_template.render(**context)
        # )
        
        raise NotImplementedError("Método pendiente de implementar")
    
    # =========================================================================
    # EMAILS DE ORDEN
    # =========================================================================
    
    async def send_order_confirmation(self, order: dict) -> EmailResult:
        """
        Envía email de confirmación de orden.
        
        Args:
            order: Datos de la orden
            
        Template variables:
        - order_number: Número de orden
        - customer_name: Nombre del cliente
        - items: Lista de items
        - total: Total de la orden
        - shipping_address: Dirección de envío
        """
        # TODO: Implementar
        # 
        # context = {
        #     "order_number": order["order_number"],
        #     "customer_name": order["customer_name"],
        #     "items": order["items"],
        #     "subtotal": order["subtotal"],
        #     "shipping_cost": order["shipping_cost"],
        #     "total": order["total"],
        #     "shipping_address": order["shipping_address"]
        # }
        # 
        # html, text = self._render_template("order_confirmation", context)
        # 
        # message = EmailMessage(
        #     to=order["customer_email"],
        #     subject=f"Confirmación de orden #{order['order_number']}",
        #     html_content=html,
        #     text_content=text
        # )
        # 
        # return await self.provider.send(message)
        
        raise NotImplementedError("Método pendiente de implementar")
    
    async def send_order_shipped(
        self, 
        order: dict, 
        tracking_number: str,
        tracking_url: str = None
    ) -> EmailResult:
        """
        Envía email de orden enviada.
        
        Args:
            order: Datos de la orden
            tracking_number: Número de seguimiento
            tracking_url: URL de seguimiento
        """
        # TODO: Implementar
        raise NotImplementedError("Método pendiente de implementar")
    
    async def send_order_delivered(self, order: dict) -> EmailResult:
        """Envía email de orden entregada."""
        # TODO: Implementar
        raise NotImplementedError("Método pendiente de implementar")
    
    # =========================================================================
    # EMAILS DE PAGO
    # =========================================================================
    
    async def send_payment_confirmation(
        self, 
        order: dict, 
        payment: dict
    ) -> EmailResult:
        """
        Envía email de confirmación de pago.
        
        Args:
            order: Datos de la orden
            payment: Datos del pago
        """
        # TODO: Implementar
        raise NotImplementedError("Método pendiente de implementar")
    
    async def send_payment_failed(
        self, 
        order: dict, 
        reason: str = None
    ) -> EmailResult:
        """Envía email de pago fallido."""
        # TODO: Implementar
        raise NotImplementedError("Método pendiente de implementar")
    
    # =========================================================================
    # EMAILS DE AUTENTICACIÓN
    # =========================================================================
    
    async def send_welcome(self, user: dict) -> EmailResult:
        """
        Envía email de bienvenida a nuevo usuario.
        
        Args:
            user: Datos del usuario
        """
        # TODO: Implementar
        raise NotImplementedError("Método pendiente de implementar")
    
    async def send_email_verification(
        self, 
        email: str, 
        verification_url: str
    ) -> EmailResult:
        """
        Envía email de verificación.
        
        Args:
            email: Email a verificar
            verification_url: URL de verificación
        """
        # TODO: Implementar
        raise NotImplementedError("Método pendiente de implementar")
    
    async def send_password_reset(
        self, 
        email: str, 
        reset_url: str
    ) -> EmailResult:
        """
        Envía email de reset de contraseña.
        
        Args:
            email: Email del usuario
            reset_url: URL para resetear contraseña
        """
        # TODO: Implementar
        raise NotImplementedError("Método pendiente de implementar")
    
    # =========================================================================
    # EMAILS DE PRODUCTOS DIGITALES
    # =========================================================================
    
    async def send_download_ready(
        self, 
        order: dict, 
        download_links: list
    ) -> EmailResult:
        """
        Envía email con enlaces de descarga para productos digitales.
        
        Args:
            order: Datos de la orden
            download_links: Lista de enlaces de descarga
        """
        # TODO: Implementar
        raise NotImplementedError("Método pendiente de implementar")

