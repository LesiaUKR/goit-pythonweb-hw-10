from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from datetime import date, timedelta

from src.database.models import Contact
from src.schemas import ContactModel, ContactResponse

class ContactRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def is_contact_exists(self, email: str, phone: str) -> bool:
        result = await self.db.execute(
            select(Contact).filter(or_(Contact.email == email, Contact.phone == phone))
        )
        return result.scalar_one_or_none() is not None

    async def create_contact(self, body: ContactModel) -> Contact:
        db_contact = Contact(**body.model_dump())
        self.db.add(db_contact)
        await self.db.commit()
        await self.db.refresh(db_contact)
        return db_contact

    async def get_contacts(
        self, name: str, surname: str, email: str, skip: int, limit: int
    ) -> List[Contact]:
        query = select(Contact)
        if name:
            query = query.filter(Contact.name.contains(name))
        if surname:
            query = query.filter(Contact.surname.contains(surname))
        if email:
            query = query.filter(Contact.email.contains(email))
        result = await self.db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

    async def get_contact_by_id(self, contact_id: int) -> Contact:
        result = await self.db.execute(select(Contact).filter(Contact.id == contact_id))
        return result.scalar_one_or_none()

    async def update_contact(self, contact_id: int, body: ContactModel) -> Contact:
        db_contact = await self.get_contact_by_id(contact_id)
        if db_contact:
            for key, value in body.model_dump().items():
                setattr(db_contact, key, value)
            await self.db.commit()
            await self.db.refresh(db_contact)
        return db_contact

    async def remove_contact(self, contact_id: int) -> Contact:
        db_contact = await self.get_contact_by_id(contact_id)
        if db_contact:
            await self.db.delete(db_contact)
            await self.db.commit()
        return db_contact

    async def get_upcoming_birthdays(self, days: int) -> List[Contact]:
        today = date.today()
        end_date = today + timedelta(days=days)
        result = await self.db.execute(
            select(Contact).filter(
                and_(
                    Contact.birthday >= today,
                    Contact.birthday <= end_date,
                )
            )
        )
        return result.scalars().all()