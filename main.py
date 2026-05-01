from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine, Base
from models import Contact
from schemas import ContactCreate, ContactUpdate, Contact
from crud import (
    get_contacts, get_contact, create_contact, update_contact, delete_contact,
    search_contacts, get_upcoming_birthdays
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Contacts API", description="API for managing contacts")

@app.get("/contacts/", response_model=list[Contact])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = get_contacts(db=db, skip=skip, limit=limit)
    return contacts

@app.get("/contacts/{contact_id}", response_model=Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = get_contact(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.post("/contacts/", response_model=Contact)
def create_new_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return create_contact(db=db, contact=contact)

@app.put("/contacts/{contact_id}", response_model=Contact)
def update_existing_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    db_contact = update_contact(db=db, contact_id=contact_id, contact=contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.delete("/contacts/{contact_id}")
def delete_existing_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = delete_contact(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted"}

@app.get("/contacts/search/", response_model=list[Contact])
def search_contacts_endpoint(query: str, db: Session = Depends(get_db)):
    contacts = search_contacts(db=db, query=query)
    return contacts

@app.get("/contacts/birthdays/", response_model=list[Contact])
def get_birthdays(db: Session = Depends(get_db)):
    contacts = get_upcoming_birthdays(db=db)
    return contacts