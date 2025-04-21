from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, nullable=True) 
    birthday = Column(Date)
    is_verified = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    created_at = Column(Date, default=func.now()) 
    updated_at = Column(Date, default=func.now(), onupdate=func.now())  

    user = relationship("User", back_populates="contacts")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)  
    avatar_url = Column(String, nullable=True)

    created_at = Column(Date, default=func.now())  
    updated_at = Column(Date, default=func.now(), onupdate=func.now())  

    contacts = relationship("Contact", back_populates="user")
