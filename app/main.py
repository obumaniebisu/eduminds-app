# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.security import hash_password  # import our hashing function

app = FastAPI(title="Eduminds API")

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

@app.get("/")
def root():
    return {"message": "Eduminds backend running"}

@app.post("/auth/register")
def register(request: RegisterRequest):
    # Hash the password
    hashed_password = hash_password(request.password)

    # For now, just return the hashed password along with other user info
    return {
        "message": "Registration successful",
        "user": {
            "username": request.username,
            "email": request.email,
            "hashed_password": hashed_password
        }
    }
