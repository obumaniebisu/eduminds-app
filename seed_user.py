from app.database import SessionLocal, engine
from app.models import User
from app.auth import get_password_hash

def create_admin():
    db = SessionLocal()
    # Check if admin already exists
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        new_admin = User(
            username="admin",
            email="admin@eduminds.com",
            hashed_password=get_password_hash("password123"), # Change this password!
            is_admin=True,
            role="admin"
        )
        db.add(new_admin)
        db.commit()
        print("Admin user created successfully!")
    else:
        print("Admin user already exists.")
    db.close()

if __name__ == "__main__":
    create_admin()