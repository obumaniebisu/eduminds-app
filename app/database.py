import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load variables from .env if it exists
load_dotenv()

# 1. Look for a DATABASE_URL from Azure. 
# If not found, default to your local SQLite file.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./eduminds.db")

# 2. Setup the engine
# 'check_same_thread' is only required for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 3. Database connection helper
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()