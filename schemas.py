from pydantic import BaseModel, EmailStr
from datetime import date

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date

class ContactCreate(ContactBase):
    pass

class ContactRead(ContactBase):
    id: int

    class Config:
        orm_mode = True
