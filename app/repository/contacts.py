from sqlalchemy.orm import Session
from app.models import Contact
from app.schemas import ContactCreate
from typing import List, Optional
from datetime import date, timedelta

def create_contact(db: Session, contact: ContactCreate) -> Contact:
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contact(db: Session, contact_id: int) -> Optional[Contact]:
    return db.query(Contact).filter(Contact.id == contact_id).first()

def get_all_contacts(
    db: Session,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None
) -> List[Contact]:
    query = db.query(Contact)
    if first_name:
        query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    return query.all()

def update_contact(db: Session, contact_id: int, contact: ContactCreate) -> Optional[Contact]:
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int) -> Optional[Contact]:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

def get_birthdays_7_days(db: Session) -> List[Contact]:
    today = date.today()
    upcoming = today + timedelta(days=7)
    return db.query(Contact).filter(
        Contact.birthday >= today,
        Contact.birthday <= upcoming
    ).all()
