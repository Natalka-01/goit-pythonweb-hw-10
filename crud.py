from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from datetime import date, timedelta
from models import Contact
from schemas import ContactCreate, ContactUpdate

def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Contact).offset(skip).limit(limit).all()

def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, contact: ContactUpdate):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact

def search_contacts(db: Session, query: str):
    return db.query(Contact).filter(
        or_(
            Contact.first_name.ilike(f"%{query}%"),
            Contact.last_name.ilike(f"%{query}%"),
            Contact.email.ilike(f"%{query}%")
        )
    ).all()

from sqlalchemy import func

def get_upcoming_birthdays(db: Session):
    today = date.today()
    next_week = today + timedelta(days=7)
    
    # Get all contacts
    all_contacts = db.query(Contact).all()
    
    upcoming_birthdays = []
    for contact in all_contacts:
        if contact.birthday:
            # Calculate next birthday
            birthday_this_year = contact.birthday.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)
            
            # Check if it's within the next 7 days
            if today <= birthday_this_year <= next_week:
                upcoming_birthdays.append(contact)
    
    return upcoming_birthdays