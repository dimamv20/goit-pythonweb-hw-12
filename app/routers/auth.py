from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User
from app.crud import get_user_by_email
from app.schemas import UserRead
from auth import verify_token
from app.database import SessionLocal

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
