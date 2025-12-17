from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

router = APIRouter()
users = []

class User(BaseModel):
    name: str
    email: str
    password: str

@router.post('/register')
def register(user: User):
    if any(u['email'] == user.email for u in users):
        raise HTTPException(status_code=400, detail='Email already registered')
    users.append(user.dict())
    return {'message': 'User registered successfully'}

def get_current_user():
    if not users:
        raise HTTPException(status_code=401, detail='Not authenticated')
    return users[0]
