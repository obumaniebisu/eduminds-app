# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.security import hash_password  # your hashing function

# FastAPI app instance
app = FastAPI(title="Eduminds API")

# Allow CORS for all origins (needed if frontend hosted elsewhere)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for registration request
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

# Root endpoint for quick test
@app.get("/")
def root():
    return {"message": "Eduminds backend running"}

# Health check endpoint (Azure will probe this)
@app.get("/health")
def health():
    return {"status": "healthy"}  # must return fast and 200 OK

# Registration endpoint
@app.post("/auth/register")
def register(request: RegisterRequest):
    # Hash password before returning (or saving to DB in future)
    hashed_pw = hash_password(request.password)
    return {
        "message": "Registration successful",
        "user": {
            "username": request.username,
            "email": request.email,
            "hashed_password": hashed_pw,
        },
    }
