from sqlalchemy.orm import Session
from models import Contact
from schemas import ContactCreate
from datetime import date, timedelta

def get_all_contacts(db: Session, first_name=None, last_name=None, email=None):
    query = db.query(Contact)
    if first_name:
        query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    return query.all()

def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

def create_contact(db: Session, contact: ContactCreate):
    new_contact = Contact(**contact.dict())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

def delete_contact(db: Session, contact_id: int):
    contact = get_contact(db, contact_id)
    if contact:
        db.delete(contact)
        db.commit()
    return contact

def update_contact(db: Session, contact_id: int, contact_data: ContactCreate):
    contact = get_contact(db, contact_id)
    if contact:
        for key, value in contact_data.dict().items():
            setattr(contact, key, value)
        db.commit()
        db.refresh(contact)
    return contact

def get_birthdays_7_days(db: Session):
    today = date.today()
    next_week = today + timedelta(days=7)
    contacts = db.query(Contact).all()
    result = []
    for c in contacts:
        bday_this_year = c.birthday.replace(year=today.year)
        if today <= bday_this_year <= next_week:
            result.append(c)
    return result
