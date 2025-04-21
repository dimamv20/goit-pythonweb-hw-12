from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import ContactCreate, ContactRead
from app.crud import (
    create_contact,
    get_all_contacts,
    get_contact,
    update_contact,
    delete_contact,
    get_birthdays_7_days,
)
from typing import List

router = APIRouter(prefix="/contacts", tags=["contacts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ContactRead)
def create(contact: ContactCreate, db: Session = Depends(get_db)):
    return create_contact(db, contact)

@router.get("/", response_model=List[ContactRead])
def read_all(first_name: str = None, last_name: str = None, email: str = None, db: Session = Depends(get_db)):
    return get_all_contacts(db, first_name, last_name, email)

@router.get("/{contact_id}", response_model=ContactRead)
def read_one(contact_id: int, db: Session = Depends(get_db)):
    contact = get_contact(db, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=ContactRead)
def update(contact_id: int, contact: ContactCreate, db: Session = Depends(get_db)):
    return update_contact(db, contact_id, contact)

@router.delete("/{contact_id}")
def delete(contact_id: int, db: Session = Depends(get_db)):
    contact = delete_contact(db, contact_id)
    if contact:
        return {"message": "Deleted"}
    raise HTTPException(status_code=404, detail="Not found")

@router.get("/birthdays/upcoming", response_model=List[ContactRead])
def upcoming_birthdays(db: Session = Depends(get_db)):
    return get_birthdays_7_days(db)
