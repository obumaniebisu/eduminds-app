# app/auth/schemas.py
from pydantic import BaseModel

# Schema for user registration request
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# Schema for user response
class UserResponse(BaseModel):
    username: str
    email: str
