from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

def hash_password(password: str) -> str:
    password = password[:72]  # truncate to 72 characters
    return pwd_context.hash(password)
