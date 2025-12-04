"""
Servicio de gestión de carritos.

Maneja todas las operaciones del carrito usando Redis
para almacenamiento rápido y eficiente.
"""

import json
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

import redis.asyncio as redis

from app.config import settings


class CartItem:
    """
    Representa un item en el carrito.
    
    CAMPOS:
    - product_id: ID del producto
    - variant_id: ID de la variante (opcional)
    - quantity: Cantidad
    - price: Precio unitario (snapshot al agregar)
    - name: Nombre del producto (snapshot)
    - image_url: URL de imagen (snapshot)
    - added_at: Fecha de agregado
    """
    
    def __init__(
        self,
        product_id: str,
        quantity: int,
        price: Decimal,
        name: str,
        image_url: Optional[str] = None,
        variant_id: Optional[str] = None,
        added_at: Optional[datetime] = None
    ):
        self.product_id = product_id
        self.variant_id = variant_id
        self.quantity = quantity
        self.price = price
        self.name = name
        self.image_url = image_url
        self.added_at = added_at or datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convierte a diccionario para almacenar en Redis."""
        return {
            "product_id": self.product_id,
            "variant_id": self.variant_id,
            "quantity": self.quantity,
            "price": str(self.price),
            "name": self.name,
            "image_url": self.image_url,
            "added_at": self.added_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "CartItem":
        """Crea instancia desde diccionario."""
        return cls(
            product_id=data["product_id"],
            variant_id=data.get("variant_id"),
            quantity=data["quantity"],
            price=Decimal(data["price"]),
            name=data["name"],
            image_url=data.get("image_url"),
            added_at=datetime.fromisoformat(data["added_at"])
        )
    
    @property
    def total(self) -> Decimal:
        """Calcula el total del item."""
        return self.price * self.quantity
    
    @property
    def item_key(self) -> str:
        """Genera la key única del item (producto + variante)."""
        if self.variant_id:
            return f"{self.product_id}:{self.variant_id}"
        return self.product_id


class CartService:
    """
    Servicio para gestión de carritos con Redis.
    
    OPERACIONES:
    - get_cart: Obtener contenido del carrito
    - add_item: Agregar producto
    - update_quantity: Actualizar cantidad
    - remove_item: Eliminar producto
    - clear_cart: Vaciar carrito
    - merge_carts: Combinar carritos
    
    ALMACENAMIENTO:
    - Key: cart:{user_id} o cart:{session_id}
    - Tipo: Hash de Redis
    - TTL: Configurable (default 7 días)
    """
    
    # Prefijo para keys de carrito
    CART_PREFIX = "cart:"
    
    # TTL por defecto (7 días en segundos)
    DEFAULT_TTL = 7 * 24 * 60 * 60
    
    def __init__(self, redis_client: redis.Redis):
        """
        Inicializa el servicio con un cliente Redis.
        
        Args:
            redis_client: Cliente Redis conectado
        """
        self.redis = redis_client
    
    def _get_cart_key(self, identifier: str) -> str:
        """
        Genera la key de Redis para un carrito.
        
        Args:
            identifier: user_id o session_id
            
        Returns:
            Key de Redis (ej: "cart:user_123")
        """
        return f"{self.CART_PREFIX}{identifier}"
    
    # =========================================================================
    # OBTENER CARRITO
    # =========================================================================
    
    async def get_cart(self, identifier: str) -> list[CartItem]:
        """
        Obtiene todos los items del carrito.
        
        IMPLEMENTACIÓN:
        1. Obtener todos los campos del hash
        2. Deserializar cada item
        3. Retornar lista de CartItem
        
        Args:
            identifier: user_id o session_id
            
        Returns:
            Lista de items en el carrito
        """
        # TODO: Implementar
        # 
        # cart_key = self._get_cart_key(identifier)
        # 
        # # Obtener todos los items del hash
        # items_raw = await self.redis.hgetall(cart_key)
        # 
        # items = []
        # for item_key, item_data in items_raw.items():
        #     data = json.loads(item_data)
        #     items.append(CartItem.from_dict(data))
        # 
        # return items
        
        raise NotImplementedError("Método pendiente de implementar")
    
    async def get_cart_summary(self, identifier: str) -> dict:
        """
        Obtiene un resumen del carrito.
        
        Returns:
            {
                "items": [...],
                "items_count": 3,
                "subtotal": 250.00
            }
        """
        # TODO: Implementar
        # 
        # items = await self.get_cart(identifier)
        # 
        # total_quantity = sum(item.quantity for item in items)
        # subtotal = sum(item.total for item in items)
        # 
        # return {
        #     "items": [item.to_dict() for item in items],
        #     "items_count": total_quantity,
        #     "subtotal": float(subtotal)
        # }
        
        raise NotImplementedError("Método pendiente de implementar")
    
    # =========================================================================
    # AGREGAR ITEM
    # =========================================================================
    
    async def add_item(
        self,
        identifier: str,
        product_id: str,
        quantity: int,
        price: Decimal,
        name: str,
        image_url: Optional[str] = None,
        variant_id: Optional[str] = None
    ) -> CartItem:
        """
        Agrega un producto al carrito.
        
        Si el producto ya existe, incrementa la cantidad.
        
        IMPLEMENTACIÓN:
        1. Generar key del item
        2. Verificar si ya existe en el carrito
        3. Si existe: incrementar cantidad
        4. Si no existe: crear nuevo item
        5. Guardar en Redis
        6. Actualizar TTL
        
        Args:
            identifier: user_id o session_id
            product_id: ID del producto
            quantity: Cantidad a agregar
            price: Precio unitario actual
            name: Nombre del producto
            image_url: URL de imagen
            variant_id: ID de variante (opcional)
            
        Returns:
            Item agregado/actualizado
            
        TODO:
        - Validar stock disponible antes de agregar
        - Validar cantidad máxima por producto
        """
        # TODO: Implementar
        # 
        # cart_key = self._get_cart_key(identifier)
        # item_key = f"{product_id}:{variant_id}" if variant_id else product_id
        # 
        # # Verificar si ya existe
        # existing = await self.redis.hget(cart_key, item_key)
        # 
        # if existing:
        #     # Actualizar cantidad
        #     item_data = json.loads(existing)
        #     item = CartItem.from_dict(item_data)
        #     item.quantity += quantity
        # else:
        #     # Crear nuevo item
        #     item = CartItem(
        #         product_id=product_id,
        #         quantity=quantity,
        #         price=price,
        #         name=name,
        #         image_url=image_url,
        #         variant_id=variant_id
        #     )
        # 
        # # Guardar en Redis
        # await self.redis.hset(cart_key, item_key, json.dumps(item.to_dict()))
        # 
        # # Actualizar TTL
        # await self.redis.expire(cart_key, self.DEFAULT_TTL)
        # 
        # return item
        
        raise NotImplementedError("Método pendiente de implementar")
    
    # =========================================================================
    # ACTUALIZAR CANTIDAD
    # =========================================================================
    
    async def update_quantity(
        self,
        identifier: str,
        product_id: str,
        quantity: int,
        variant_id: Optional[str] = None
    ) -> Optional[CartItem]:
        """
        Actualiza la cantidad de un producto.
        
        Si quantity = 0, elimina el producto.
        
        Args:
            identifier: user_id o session_id
            product_id: ID del producto
            quantity: Nueva cantidad
            variant_id: ID de variante (opcional)
            
        Returns:
            Item actualizado o None si se eliminó
            
        TODO:
        - Validar stock disponible
        - Validar cantidad mínima (1) y máxima
        """
        # TODO: Implementar
        # 
        # if quantity <= 0:
        #     await self.remove_item(identifier, product_id, variant_id)
        #     return None
        # 
        # cart_key = self._get_cart_key(identifier)
        # item_key = f"{product_id}:{variant_id}" if variant_id else product_id
        # 
        # existing = await self.redis.hget(cart_key, item_key)
        # if not existing:
        #     return None
        # 
        # item_data = json.loads(existing)
        # item = CartItem.from_dict(item_data)
        # item.quantity = quantity
        # 
        # await self.redis.hset(cart_key, item_key, json.dumps(item.to_dict()))
        # await self.redis.expire(cart_key, self.DEFAULT_TTL)
        # 
        # return item
        
        raise NotImplementedError("Método pendiente de implementar")
    
    # =========================================================================
    # ELIMINAR ITEM
    # =========================================================================
    
    async def remove_item(
        self,
        identifier: str,
        product_id: str,
        variant_id: Optional[str] = None
    ) -> bool:
        """
        Elimina un producto del carrito.
        
        Args:
            identifier: user_id o session_id
            product_id: ID del producto
            variant_id: ID de variante (opcional)
            
        Returns:
            True si se eliminó, False si no existía
        """
        # TODO: Implementar
        # 
        # cart_key = self._get_cart_key(identifier)
        # item_key = f"{product_id}:{variant_id}" if variant_id else product_id
        # 
        # result = await self.redis.hdel(cart_key, item_key)
        # return result > 0
        
        raise NotImplementedError("Método pendiente de implementar")
    
    # =========================================================================
    # VACIAR CARRITO
    # =========================================================================
    
    async def clear_cart(self, identifier: str) -> bool:
        """
        Vacía completamente el carrito.
        
        Args:
            identifier: user_id o session_id
            
        Returns:
            True si se vació, False si ya estaba vacío
        """
        # TODO: Implementar
        # 
        # cart_key = self._get_cart_key(identifier)
        # result = await self.redis.delete(cart_key)
        # return result > 0
        
        raise NotImplementedError("Método pendiente de implementar")
    
    # =========================================================================
    # MERGE DE CARRITOS
    # =========================================================================
    
    async def merge_carts(
        self,
        source_identifier: str,
        target_identifier: str,
        strategy: str = "combine"
    ) -> list[CartItem]:
        """
        Combina dos carritos (usado al hacer login).
        
        Cuando un usuario anónimo hace login, su carrito
        de sesión se combina con su carrito de usuario.
        
        ESTRATEGIAS:
        - "combine": Suma cantidades si hay duplicados
        - "replace": El carrito fuente reemplaza items duplicados
        - "keep_target": Mantiene items del carrito destino en duplicados
        
        Args:
            source_identifier: session_id (carrito anónimo)
            target_identifier: user_id (carrito del usuario)
            strategy: Estrategia de merge
            
        Returns:
            Items del carrito combinado
        """
        # TODO: Implementar
        # 
        # source_items = await self.get_cart(source_identifier)
        # target_items = await self.get_cart(target_identifier)
        # 
        # # Crear diccionario de items del target
        # target_dict = {item.item_key: item for item in target_items}
        # 
        # for source_item in source_items:
        #     key = source_item.item_key
        #     
        #     if key in target_dict:
        #         if strategy == "combine":
        #             target_dict[key].quantity += source_item.quantity
        #         elif strategy == "replace":
        #             target_dict[key] = source_item
        #         # "keep_target" no hace nada
        #     else:
        #         target_dict[key] = source_item
        # 
        # # Guardar carrito combinado
        # cart_key = self._get_cart_key(target_identifier)
        # await self.redis.delete(cart_key)
        # 
        # for item in target_dict.values():
        #     await self.redis.hset(
        #         cart_key, 
        #         item.item_key, 
        #         json.dumps(item.to_dict())
        #     )
        # 
        # await self.redis.expire(cart_key, self.DEFAULT_TTL)
        # 
        # # Eliminar carrito fuente
        # await self.clear_cart(source_identifier)
        # 
        # return list(target_dict.values())
        
        raise NotImplementedError("Método pendiente de implementar")
    
    # =========================================================================
    # UTILIDADES
    # =========================================================================
    
    async def get_item_count(self, identifier: str) -> int:
        """
        Obtiene la cantidad total de items (suma de quantities).
        
        Útil para mostrar el badge del carrito.
        """
        # TODO: Implementar
        # 
        # items = await self.get_cart(identifier)
        # return sum(item.quantity for item in items)
        
        raise NotImplementedError("Método pendiente de implementar")
    
    async def item_exists(
        self,
        identifier: str,
        product_id: str,
        variant_id: Optional[str] = None
    ) -> bool:
        """
        Verifica si un producto está en el carrito.
        """
        # TODO: Implementar
        # 
        # cart_key = self._get_cart_key(identifier)
        # item_key = f"{product_id}:{variant_id}" if variant_id else product_id
        # 
        # return await self.redis.hexists(cart_key, item_key)
        
        raise NotImplementedError("Método pendiente de implementar")

