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

# OrderItem and Order schemas can be added later
