from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import ContactCreate, Token
from crud import create_contact, authenticate_contact
from auth import create_access_token
from database import get_db

router = APIRouter()

@router.post("/register", response_model=Token)
def register(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = authenticate_contact(db, contact.email, contact.password)
    if db_contact:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_contact = create_contact(db, contact)
    access_token = create_access_token(data={"sub": new_contact.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = authenticate_contact(db, contact.email, contact.password)
    if db_contact is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_contact.email})
    return {"access_token": access_token, "token_type": "bearer"}
