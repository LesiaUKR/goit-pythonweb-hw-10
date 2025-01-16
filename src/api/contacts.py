from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from datetime import date

from src.schemas import ContactModel, ContactResponse
from src.database.database import get_db
from src.services.contacts import ContactService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/contacts/", response_model=ContactResponse)
async def create_contact(
    body: ContactModel, db: AsyncSession = Depends(get_db)
):
    service = ContactService(db)
    return await service.create_contact(body)

@router.get("/contacts/", response_model=List[ContactResponse])
async def read_contacts(
    name: str = Query(None),
    surname: str = Query(None),
    email: str = Query(None),
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    service = ContactService(db)
    return await service.get_contacts(name, surname, email, skip, limit)

@router.get("/contacts/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    return await service.get_contact(contact_id)

@router.put("/contacts/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int, body: ContactModel, db: AsyncSession = Depends(get_db)
):
    service = ContactService(db)
    return await service.update_contact(contact_id, body)

@router.delete("/contacts/{contact_id}", response_model=ContactResponse)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    return await service.remove_contact(contact_id)

@router.get("/contacts/birthdays/", response_model=List[ContactResponse])
async def upcoming_birthdays(days: int = 7, db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    return await service.get_upcoming_birthdays(days)