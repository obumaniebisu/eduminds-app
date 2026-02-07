# app/main.py
import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.security import hash_password  # make sure this exists and works

app = FastAPI(title="Eduminds API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic schema for registration input
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

# Root endpoint
@app.get("/")
def root():
    return {"message": "Eduminds backend running"}

# Health check endpoint for Azure
@app.get("/health")
def health():
    return {"status": "healthy"}

# Registration endpoint
@app.post("/auth/register")
def register(request: RegisterRequest):
    hashed_password = hash_password(request.password)
    return {
        "message": "Registration successful",
        "user": {
            "username": request.username,
            "email": request.email,
            "hashed_password": hashed_password
        }
    }

# Azure requires the app to bind to the PORT environment variable
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
