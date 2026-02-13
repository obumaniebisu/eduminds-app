# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.security import hash_password

app = FastAPI(title="Eduminds API")

# Allow all CORS requests (good for testing, can restrict later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registration input schema
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

@app.get("/")
def root():
    return {"message": "Eduminds backend running"}

# Azure Health Check endpoint
@app.get("/health")
def health():
    """
    Simple health check for Azure App Service
    Returns 200 OK if the app is running
    """
    return {"status": "healthy"}

@app.post("/auth/register")
def register(request: RegisterRequest):
    # Hash the password
    hashed_password = hash_password(request.password)

    return {
        "message": "Registration successful",
        "user": {
            "username": request.username,
            "email": request.email,
            "hashed_password": hashed_password,
        },
    }
