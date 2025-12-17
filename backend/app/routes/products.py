from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Product(BaseModel):
    id: int
    name: str
    price: float

products = [
    {'id': 1, 'name': 'Python Course', 'price': 50.0},
    {'id': 2, 'name': 'FastAPI Course', 'price': 75.0},
]

@router.get('/')
def get_products():
    return products
