from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Contacts API!"}

class Contact(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: str

contacts = [
    Contact(id=1, first_name="John", last_name="Doe", email="john.doe@example.com", phone="123-456-7890", birthday="1990-05-15"),
    Contact(id=2, first_name="Jane", last_name="Smith", email="jane.smith@example.com", phone="987-654-3210", birthday="1985-12-30")
]

@app.get("/contacts", response_model=List[Contact])
def get_contacts():
    return contacts

@app.get("/contacts/{contact_id}", response_model=Contact)
def get_contact(contact_id: int):
    contact = next((c for c in contacts if c.id == contact_id), None)
    if contact:
        return contact
    return {"error": "Contact not found"}

@app.post("/contacts", response_model=Contact)
def create_contact(contact: Contact):
    contacts.append(contact)
    return contact

@app.put("/contacts/{contact_id}", response_model=Contact)
def update_contact(contact_id: int, contact: Contact):
    for i, c in enumerate(contacts):
        if c.id == contact_id:
            contacts[i] = contact
            return contact
    return {"error": "Contact not found"}

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):
    global contacts
    contacts = [c for c in contacts if c.id != contact_id]
    return {"message": "Contact deleted successfully"}
