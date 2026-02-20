from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

# Internal imports from your other files
from . import models
from .database import engine, get_db
from .security import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM

# 1. Initialize Database Tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Eduminds API")

# 2. Tell FastAPI where to find the "Lock" (OAuth2)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Schemas ---
class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# --- THE SECURITY GUARD (Dependency) ---
# This function checks the "Digital Key" (Token)
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Decode the token to see who it belongs to
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid Token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token has expired or is invalid")
        
    user = db.query(models.User).filter(models.User.email == email).first()
    return user

# --- ENDPOINTS ---

@app.post("/auth/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # Standard registration logic
    hashed_pwd = hash_password(request.password)
    new_user = models.User(username=request.username, email=request.email, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    return {"message": "User registered!"}

@app.post("/auth/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong email or password")

    # GIVE THE USER THEIR KEY
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# --- THE LOCKED ROOM (Protected Route) ---
@app.get("/users/me")
def read_users_me(current_user: models.User = Depends(get_current_user)):
    # This only runs if get_current_user finds a valid key!
    return {
        "msg": "Welcome to your private dashboard",
        "user_details": {
            "username": current_user.username,
            "email": current_user.email
        }
    }