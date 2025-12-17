from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from app.routes.products import products
from app.routes.users import get_current_user

router = APIRouter()
orders = []

class Order(BaseModel):
    product_ids: List[int]

@router.get('/')
def get_orders():
    return orders

@router.post('/')
def add_order(order: Order, current_user: dict = Depends(get_current_user)):
    for pid in order.product_ids:
        if not any(p['id'] == pid for p in products):
            raise HTTPException(status_code=400, detail=f'Product ID {pid} does not exist')
    order_id = len(orders) + 1
    total_price = sum(p['price'] for p in products if p['id'] in order.product_ids)
    new_order = {
        'id': order_id,
        'product_ids': order.product_ids,
        'total_price': total_price,
        'user': current_user['email']
    }
    orders.append(new_order)
    return {'message': 'Order created', 'order': new_order}
