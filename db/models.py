from dataclasses import dataclass


@dataclass
class Product:
    id: int
    name: str
    category: str
    price: float
    description: str
    stock: int
    rating: float
    created_at: str = ""


@dataclass
class Order:
    id: int
    product_id: int
    product_name: str
    quantity: int
    total_price: float
    status: str
    created_at: str = ""
