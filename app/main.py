from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Internal imports
from . import models
from .database import engine, get_db
from .security import hash_password, verify_password # Added verify_password

# Create database tables automatically on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Eduminds API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Input Schemas ---
class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# --- Endpoints ---

@app.get("/")
def root():
    return {"message": "Eduminds backend running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/auth/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # 1. Check if user already exists
    existing_user = db.query(models.User).filter(models.User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Hash and Save
    hashed_pwd = hash_password(request.password)
    new_user = models.User(
        username=request.username, 
        email=request.email, 
        hashed_password=hashed_pwd
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered and saved!", 
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }
    }

@app.post("/auth/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # 1. Fetch the user
    user = db.query(models.User).filter(models.User.email == request.email).first()
    
    # 2. Validate user existence and password
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=401, 
            detail="Invalid email or password"
        )

    return {
        "message": "Login successful",
        "user": {
            "username": user.username,
            "email": user.email
        }
    }