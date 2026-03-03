from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, EmailStr

# Internal imports
from app import models, auth, database

# 1. Initialize database tables
models.Base.metadata.create_all(bind=database.engine)

# 2. SEED ADMIN USER (Azure-Safe: includes email to avoid NOT NULL errors)
def seed_admin():
    db = database.SessionLocal()
    try:
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        if not admin:
            new_admin = models.User(
                username="admin",
                email="admin@eduminds.com",
                hashed_password=auth.get_password_hash("admin123"),
                role="admin",
                is_admin=True
            )
            db.add(new_admin)
            db.commit()
            print("--- Admin user 'admin' created ---")
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
    return {"status": "healthy", "version": "1.1.0", "tier": "Azure-Free-Optimized"}

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

# --- 6. ADMIN DASHBOARD & PAGINATED LISTS ---
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

@app.get("/admin/students")
def list_students(
    skip: int = 0, 
    limit: int = Query(default=10, le=50), # Pagination: Max 50 per request
    db: Session = Depends(database.get_db),
    current_admin: models.User = Depends(auth.admin_required)
):
    """Azure-Safe: Loads only 10 students at a time to save memory."""
    students = db.query(models.Student).offset(skip).limit(limit).all()
    return students

# --- 7. STUDENT MANAGEMENT (CRUD) ---
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

@app.put("/admin/students/{student_id}")
def update_student(
    student_id: int, 
    student_update: StudentCreate, 
    db: Session = Depends(database.get_db),
    current_admin: models.User = Depends(auth.admin_required)
):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    for key, value in student_update.model_dump().items():
        setattr(db_student, key, value)
    
    db.commit()
    db.refresh(db_student)
    return {"message": "Student updated", "student": db_student}

@app.delete("/admin/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student_id: int, 
    db: Session = Depends(database.get_db),
    current_admin: models.User = Depends(auth.admin_required)
):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(db_student)
    db.commit()
    return None

# --- 8. SKILL MANAGEMENT (CRUD) ---
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

@app.delete("/admin/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(
    skill_id: int, 
    db: Session = Depends(database.get_db),
    current_admin: models.User = Depends(auth.admin_required)
):
    db_skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    # Safety Check: Prevent orphaned student records
    has_students = db.query(models.Student).filter(models.Student.skill_id == skill_id).first()
    if has_students:
        raise HTTPException(status_code=400, detail="Cannot delete skill: students are enrolled.")
    
    db.delete(db_skill)
    db.commit()
    return None