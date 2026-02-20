from datetime import datetime, timedelta
from typing import Optional
from jose import jwt # This handles the "Signing" of the token
from passlib.context import CryptContext

# --- CONFIGURATION (In a real app, move these to a .env file!) ---
SECRET_KEY = "SUPER_SECRET_EDUMINDS_KEY_123" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # Your logic: Truncate to 72 to align with bcrypt's internal limit
    return pwd_context.hash(password[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password[:72], hashed_password)

# --- NEW: JWT Logic ---
def create_access_token(data: dict):
    """
    Creates an encrypted digital "wristband" for the user.
    """
    to_encode = data.copy()
    
    # Set the token to expire 30 minutes from now
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Encrypt the data with our SECRET_KEY
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt