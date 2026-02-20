# app/security.py
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

def hash_password(password: str) -> str:
    # Truncate to 72 to align with bcrypt's internal limit
    password = password[:72]  
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks if the plain text password matches the stored hash.
    """
    return pwd_context.verify(plain_password[:72], hashed_password)