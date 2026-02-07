# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.security import hash_password

app = FastAPI(title="Eduminds API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

@app.get("/")
def root():
    return {"message": "Eduminds backend running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/auth/register")
def register(request: RegisterRequest):
    return {
        "message": "Registration successful",
        "user": {
            "username": request.username,
            "email": request.email,
            "hashed_password": hash_password(request.password),
        },
    }
