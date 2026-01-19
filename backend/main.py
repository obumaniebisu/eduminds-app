from fastapi import FastAPI

app = FastAPI(title="Eduminds Backend")  # only once

# Temporarily comment out routers for Azure deployment
# from backend.orders import router as orders_router
# app.include_router(orders_router, prefix="/orders")

# Root endpoint to test app startup
@app.get("/")
def root():
    return {"message": "Eduminds backend running"}
