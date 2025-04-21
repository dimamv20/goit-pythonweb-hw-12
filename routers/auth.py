from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from crud import get_user_by_email
from schemas import UserRead
from auth import verify_token
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/me", response_model=UserRead)
def get_me(token: str = Depends(verify_token), db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=token)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
