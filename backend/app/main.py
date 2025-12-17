from fastapi import FastAPI
from app.routes.users import router as user_router
from app.routes.products import router as product_router
from app.routes.orders import router as order_router

app = FastAPI(title="Eduminds API")

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(product_router, prefix="/products", tags=["Products"])
app.include_router(order_router, prefix="/orders", tags=["Orders"])
