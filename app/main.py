from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, EmailStr

# Internal imports
from app import models, auth, database

# 1. Initialize database tables
models.Base.metadata.create_all(bind=database.engine)

# 2. SEED ADMIN USER (Prevents 401 Unauthorized)
def seed_admin():
    db = database.SessionLocal()
    try:
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        if not admin:
            new_admin = models.User(
                username="admin",
                hashed_password=auth.get_password_hash("admin123"),
                role="admin"
            )
            db.add(new_admin)
            db.commit()
            print("--- Admin user 'admin' created with password 'admin123' ---")
    finally:
        db.close()

seed_admin()

app = FastAPI(title="Eduminds Backend")

# --- 3. SCHEMAS ---
class SkillCreate(BaseModel):
    name: str
    description: Optional[str] = None

class StudentCreate(BaseModel):
    full_name: str
    email: EmailStr
    enrollment_id: str
    skill_id: int

# --- 4. HEALTH CHECK ---
@app.get("/")
def health_check():
    return {"status": "healthy", "version": "1.0.1"}

# --- 5. AUTHENTICATION ---
@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid username or password"
        )

    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# --- 6. ADMIN DASHBOARD ---
@app.get("/admin/dashboard")
def get_admin_dashboard(
    db: Session = Depends(database.get_db),
    current_admin: models.User = Depends(auth.admin_required)
):
    student_count = db.query(models.Student).count()
    skills = db.query(models.Skill).all()
    skill_names = [s.name for s in skills]

    return {
        "message": f"Welcome back, {current_admin.username}!",
        "stats": {
            "active_students": student_count,
            "skills": skill_names
        }
    }

# --- 7. STUDENT MANAGEMENT ---
@app.post("/admin/students", status_code=status.HTTP_201_CREATED)
def register_student(
    student: StudentCreate,
    db: Session = Depends(database.get_db),
    current_admin: models.User = Depends(auth.admin_required)
):
    if db.query(models.Student).filter(models.Student.email == student.email).first():
        raise HTTPException(status_code=400, detail="Student email already registered")

    new_student = models.Student(**student.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {"message": "Student created", "id": new_student.id}

# --- 8. SKILL MANAGEMENT ---
@app.post("/admin/skills")
def add_skill(
    skill: SkillCreate,
    db: Session = Depends(database.get_db),
    current_admin: models.User = Depends(auth.admin_required)
):
    if db.query(models.Skill).filter(models.Skill.name == skill.name).first():
        raise HTTPException(status_code=400, detail="Skill already exists")

    new_skill = models.Skill(**skill.model_dump())
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return {"message": "Skill added", "id": new_skill.id}