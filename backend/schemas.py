from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# Product Schemas
class ProductBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    class Config:
        orm_mode = True

# OrderItem Schemas
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    product: Product
    class Config:
        orm_mode = True

# Order Schemas
class OrderBase(BaseModel):
    customer_name: str
    order_date: date

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: int
    items: List[OrderItem]
    class Config:
        orm_mode = True

