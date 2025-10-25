from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Backend.core.database import get_db
from Backend.table_models.user_model import User as UserTable
from Backend.auth.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

# Create user
@router.post("/")
def create_user(email: str, password: str, db: Session = Depends(get_db)):
    existing = db.query(UserTable).filter(UserTable.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = UserTable(email=email, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "email": user.email}

# Get all users
@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(UserTable).all()
    return users
