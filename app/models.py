# app/auth/models.py
from pydantic import BaseModel

# Example user model (for demonstration)
class User(BaseModel):
    username: str
    email: str
    password: str
