from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_orders():
    return {"orders": "List of orders will appear here"}

@router.get("/{order_id}")
def get_order(order_id: int):
    return {"order_id": order_id, "details": "Order details will appear here"}
