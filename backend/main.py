from fastapi import FastAPI
from app.orders import router as orders_router
from app.products import router as products_router
from app.users import router as users_router

app = FastAPI(title="Eduminds Backend")

# Include routers
app.include_router(orders_router)
app.include_router(products_router)
app.include_router(users_router)

# Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}
