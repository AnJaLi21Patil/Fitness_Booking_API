from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db   # ✅ FIX
from app import models, schemas, auth

router = APIRouter()


@router.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=auth.hash_password(user.password)
    )
    db.add(new_user)
    db.commit()

    return {"message": "User created successfully"}


@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user or not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_access_token({"sub": db_user.email})
    return {
        "access_token": token,
        "token_type": "bearer"
    }
