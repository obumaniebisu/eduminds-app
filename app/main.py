# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.security import hash_password  # make sure app/security.py exists

app = FastAPI(title="Eduminds API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins; change for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------
# Pydantic schema
# ----------------------
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

# ----------------------
# Root endpoint
# ----------------------
@app.get("/")
def root():
    return {"message": "Eduminds backend running"}

# ----------------------
# Health check endpoint (for Azure)
# ----------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# ----------------------
# Registration endpoint
# ----------------------
@app.post("/auth/register")
def register(request: RegisterRequest):
    # Hash the password
    hashed_password = hash_password(request.password)

    # Return response
    return {
        "message": "Registration successful",
        "user": {
            "username": request.username,
            "email": request.email,
            "hashed_password": hashed_password
        }
    }

# ----------------------
# Run with uvicorn in Azure:
# uvicorn app.main:app --host 0.0.0.0 --port 8000
# ----------------------
