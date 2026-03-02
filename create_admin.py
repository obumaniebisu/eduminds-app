import sys
import os

# This ensures Python can see the 'app' folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import models, auth, database
from app.database import engine

def create_initial_admin():
    print("Connecting to database...")
    models.Base.metadata.create_all(bind=engine)
    
    db = database.SessionLocal()
    try:
        existing_admin = db.query(models.User).filter(models.User.username == "admin").first()
        
        if not existing_admin:
            print("Creating admin user with email...")
            admin_user = models.User(
                username="admin",
                email="admin@eduminds.com",  # This line fixes the error!
                hashed_password=auth.get_password_hash("admin123"),
                role="admin",
                is_admin=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ SUCCESS: Admin user 'admin' created with password 'admin123'")
        else:
            print("ℹ️ Admin already exists.")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_admin()