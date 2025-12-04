"""
Modelos de perfil de usuario y direcciones.

Este servicio extiende la información básica del usuario
que se maneja en el servicio Auth.
"""

import uuid
from datetime import datetime, date
from enum import Enum as PyEnum

from sqlalchemy import (
    Column, String, Boolean, DateTime, Date,
    ForeignKey, Enum, Text, Integer
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

# TODO: Importar Base desde database.py
# from app.database import Base
from sqlalchemy.orm import declarative_base
Base = declarative_base()


# ==============================================================================
# ENUMS
# ==============================================================================

class Gender(str, PyEnum):
    """Género del usuario (opcional)."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class AddressType(str, PyEnum):
    """Tipo de dirección."""
    SHIPPING = "shipping"      # Dirección de envío
    BILLING = "billing"        # Dirección de facturación
    BOTH = "both"              # Ambas


# ==============================================================================
# MODELO: UserProfile
# ==============================================================================

class UserProfile(Base):
    """
    Perfil extendido del usuario.
    
    Contiene información adicional que no se maneja en Auth:
    - Nombre completo
    - Teléfono
    - Fecha de nacimiento
    - Avatar
    - Preferencias
    
    CAMPOS A IMPLEMENTAR:
    """
    __tablename__ = "user_profiles"
    
    # =========================================================================
    # Identificación
    # =========================================================================
    
    # ID del usuario (mismo que en Auth service)
    # TODO: Este ID debe coincidir con el del servicio Auth
    user_id = Column(
        UUID(as_uuid=True), 
        primary_key=True,
        comment="ID del usuario (sincronizado con Auth service)"
    )
    
    # =========================================================================
    # Datos personales
    # =========================================================================
    
    # Nombre y apellido
    # TODO: Validar longitud máxima
    first_name = Column(
        String(100), 
        nullable=True,
        comment="Nombre del usuario"
    )
    
    last_name = Column(
        String(100), 
        nullable=True,
        comment="Apellido del usuario"
    )
    
    # Teléfono
    # TODO: Validar formato de teléfono
    phone = Column(
        String(20), 
        nullable=True,
        comment="Número de teléfono con código de país"
    )
    
    # Fecha de nacimiento (para promociones de cumpleaños, etc.)
    date_of_birth = Column(
        Date, 
        nullable=True,
        comment="Fecha de nacimiento"
    )
    
    # Género (opcional)
    gender = Column(
        Enum(Gender), 
        nullable=True,
        comment="Género del usuario (opcional)"
    )
    
    # =========================================================================
    # Avatar y personalización
    # =========================================================================
    
    # URL del avatar
    # TODO: Implementar upload de imágenes
    avatar_url = Column(
        String(500), 
        nullable=True,
        comment="URL de la imagen de perfil"
    )
    
    # =========================================================================
    # Preferencias
    # =========================================================================
    
    # Idioma preferido
    preferred_language = Column(
        String(10), 
        default="es",
        comment="Código de idioma preferido (es, en, etc.)"
    )
    
    # Moneda preferida
    preferred_currency = Column(
        String(3), 
        default="ARS",
        comment="Código de moneda (ARS, USD, etc.)"
    )
    
    # Acepta emails de marketing
    accepts_marketing = Column(
        Boolean, 
        default=False,
        comment="Si el usuario acepta emails promocionales"
    )
    
    # =========================================================================
    # Timestamps
    # =========================================================================
    
    created_at = Column(
        DateTime, 
        default=datetime.utcnow
    )
    
    updated_at = Column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    
    # =========================================================================
    # Relaciones
    # =========================================================================
    
    addresses = relationship(
        "Address", 
        back_populates="user_profile",
        cascade="all, delete-orphan"
    )
    
    # =========================================================================
    # Propiedades
    # =========================================================================
    
    @property
    def full_name(self) -> str:
        """Retorna el nombre completo del usuario."""
        parts = []
        if self.first_name:
            parts.append(self.first_name)
        if self.last_name:
            parts.append(self.last_name)
        return " ".join(parts) if parts else ""
    
    def __repr__(self):
        return f"<UserProfile {self.user_id}>"


# ==============================================================================
# MODELO: Address
# ==============================================================================

class Address(Base):
    """
    Dirección del usuario.
    
    Puede ser de envío, facturación o ambas.
    Un usuario puede tener múltiples direcciones.
    
    CAMPOS A IMPLEMENTAR:
    """
    __tablename__ = "addresses"
    
    # =========================================================================
    # Identificación
    # =========================================================================
    
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("user_profiles.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Usuario propietario de la dirección"
    )
    
    # =========================================================================
    # Tipo y etiqueta
    # =========================================================================
    
    # Etiqueta amigable (ej: "Casa", "Trabajo", "Casa de mamá")
    label = Column(
        String(50), 
        nullable=True,
        comment="Etiqueta para identificar la dirección"
    )
    
    # Tipo de dirección
    address_type = Column(
        Enum(AddressType), 
        default=AddressType.BOTH,
        comment="Si es de envío, facturación o ambas"
    )
    
    # =========================================================================
    # Datos del destinatario
    # =========================================================================
    
    # Nombre del destinatario (puede ser diferente al usuario)
    # TODO: Requerir este campo
    recipient_name = Column(
        String(200), 
        nullable=False,
        comment="Nombre completo del destinatario"
    )
    
    # Teléfono de contacto
    phone = Column(
        String(20), 
        nullable=True,
        comment="Teléfono de contacto para el envío"
    )
    
    # =========================================================================
    # Dirección
    # =========================================================================
    
    # Calle
    street = Column(
        String(200), 
        nullable=False,
        comment="Nombre de la calle"
    )
    
    # Número
    number = Column(
        String(20), 
        nullable=False,
        comment="Número de la dirección"
    )
    
    # Piso/Departamento (opcional)
    apartment = Column(
        String(50), 
        nullable=True,
        comment="Piso, departamento, oficina, etc."
    )
    
    # Referencias adicionales
    reference = Column(
        String(200), 
        nullable=True,
        comment="Referencias para encontrar la dirección"
    )
    
    # Ciudad
    city = Column(
        String(100), 
        nullable=False,
        comment="Ciudad"
    )
    
    # Provincia/Estado
    state = Column(
        String(100), 
        nullable=False,
        comment="Provincia o estado"
    )
    
    # Código postal
    postal_code = Column(
        String(20), 
        nullable=False,
        comment="Código postal"
    )
    
    # País
    country = Column(
        String(100), 
        default="Argentina",
        comment="País"
    )
    
    # =========================================================================
    # Datos fiscales (para facturación)
    # =========================================================================
    
    # CUIT/CUIL/DNI para facturación
    tax_id = Column(
        String(20), 
        nullable=True,
        comment="CUIT/CUIL/DNI para facturación"
    )
    
    # Razón social (para empresas)
    company_name = Column(
        String(200), 
        nullable=True,
        comment="Razón social (si es empresa)"
    )
    
    # =========================================================================
    # Estado
    # =========================================================================
    
    # Si es la dirección por defecto
    is_default = Column(
        Boolean, 
        default=False,
        comment="Si es la dirección por defecto del usuario"
    )
    
    # Si está activa (soft delete)
    is_active = Column(
        Boolean, 
        default=True,
        comment="Si la dirección está activa"
    )
    
    # =========================================================================
    # Timestamps
    # =========================================================================
    
    created_at = Column(
        DateTime, 
        default=datetime.utcnow
    )
    
    updated_at = Column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    
    # =========================================================================
    # Relaciones
    # =========================================================================
    
    user_profile = relationship("UserProfile", back_populates="addresses")
    
    # =========================================================================
    # Propiedades
    # =========================================================================
    
    @property
    def full_address(self) -> str:
        """Retorna la dirección completa formateada."""
        parts = [f"{self.street} {self.number}"]
        if self.apartment:
            parts.append(self.apartment)
        parts.append(f"{self.city}, {self.state}")
        parts.append(f"CP {self.postal_code}")
        parts.append(self.country)
        return ", ".join(parts)
    
    def __repr__(self):
        return f"<Address {self.label or self.street}>"

