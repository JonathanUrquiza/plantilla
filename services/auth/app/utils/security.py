"""
Utilidades de seguridad.

Funciones para manejo seguro de contraseñas y datos sensibles.
"""

from passlib.context import CryptContext

# ==============================================================================
# CONFIGURACIÓN DE PASSLIB
# ==============================================================================
# Usar bcrypt para hashear passwords
# bcrypt es resistente a ataques de fuerza bruta y rainbow tables

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"  # Permite migrar hashes antiguos automáticamente
)


# ==============================================================================
# FUNCIONES DE PASSWORD
# ==============================================================================

def hash_password(password: str) -> str:
    """
    Hashea una contraseña usando bcrypt.
    
    Bcrypt:
    - Incluye salt automáticamente
    - Es deliberadamente lento (resistente a brute force)
    - El costo se puede ajustar (default: 12 rounds)
    
    Args:
        password: Contraseña en texto plano
        
    Returns:
        Hash de la contraseña (incluye el salt)
        
    Ejemplo:
        hashed = hash_password("MiPassword123")
        # Resultado: "$2b$12$..."
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña coincide con su hash.
    
    Args:
        plain_password: Contraseña en texto plano a verificar
        hashed_password: Hash almacenado en BD
        
    Returns:
        True si coincide, False si no
        
    Ejemplo:
        if verify_password("MiPassword123", stored_hash):
            print("Password correcto")
    """
    return pwd_context.verify(plain_password, hashed_password)


# ==============================================================================
# FUNCIONES DE TOKENS
# ==============================================================================

def generate_random_token(length: int = 32) -> str:
    """
    Genera un token aleatorio seguro.
    
    Usa secrets.token_urlsafe que es criptográficamente seguro.
    
    Args:
        length: Longitud aproximada del token (será base64)
        
    Returns:
        Token aleatorio URL-safe
        
    Ejemplo:
        token = generate_random_token()
        # Resultado: "aB3-xY9_..."
    """
    import secrets
    return secrets.token_urlsafe(length)


def hash_token(token: str) -> str:
    """
    Hashea un token para almacenamiento.
    
    Usa SHA256 que es suficiente para tokens de alta entropía.
    NO usar para passwords (usar bcrypt para eso).
    
    Args:
        token: Token en texto plano
        
    Returns:
        Hash SHA256 del token
    """
    import hashlib
    return hashlib.sha256(token.encode()).hexdigest()


# ==============================================================================
# VALIDACIONES DE SEGURIDAD
# ==============================================================================

def validate_password_strength(password: str) -> tuple[bool, list[str]]:
    """
    Valida la fortaleza de una contraseña.
    
    Requisitos:
    - Mínimo 8 caracteres
    - Al menos una mayúscula
    - Al menos una minúscula
    - Al menos un número
    
    Args:
        password: Contraseña a validar
        
    Returns:
        Tupla (es_válida, lista_de_errores)
        
    Ejemplo:
        is_valid, errors = validate_password_strength("weak")
        if not is_valid:
            print(errors)  # ["Mínimo 8 caracteres", ...]
    """
    errors = []
    
    if len(password) < 8:
        errors.append("La contraseña debe tener al menos 8 caracteres")
    
    if not any(c.isupper() for c in password):
        errors.append("La contraseña debe contener al menos una mayúscula")
    
    if not any(c.islower() for c in password):
        errors.append("La contraseña debe contener al menos una minúscula")
    
    if not any(c.isdigit() for c in password):
        errors.append("La contraseña debe contener al menos un número")
    
    # Opcional: validar caracteres especiales
    # special_chars = "!@#$%^&*(),.?\":{}|<>"
    # if not any(c in special_chars for c in password):
    #     errors.append("La contraseña debe contener al menos un carácter especial")
    
    return (len(errors) == 0, errors)


# ==============================================================================
# SANITIZACIÓN
# ==============================================================================

def sanitize_email(email: str) -> str:
    """
    Normaliza un email para búsquedas consistentes.
    
    - Convierte a minúsculas
    - Elimina espacios
    
    Args:
        email: Email a normalizar
        
    Returns:
        Email normalizado
    """
    return email.lower().strip()

