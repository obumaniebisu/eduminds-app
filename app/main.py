# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.security import hash_password  # import our hashing function

app = FastAPI(title="Eduminds API")

# Enable CORS for all origins (you can restrict later if needed)
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
def health_check():
    # Simple response, always returns 200 OK
    return {"status": "healthy"}

# Registration endpoint
@app.post("/auth/register")
def register(request: RegisterRequest):
    # Hash the password
    hashed_password = hash_password(request.password)

    # Return user info with hashed password
    return {
        "message": "Registration successful",
        "user": {
            "username": request.username,
            "email": request.email,
            "hashed_password": hashed_password
        }
    }
