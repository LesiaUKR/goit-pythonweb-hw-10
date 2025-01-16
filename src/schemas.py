
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr, validator
import re

class ContactModel(BaseModel):
    name: str = Field(min_length=2, max_length=50, example="John")
    surname: str = Field(min_length=2, max_length=50, example="Doe")
    email: EmailStr = Field(min_length=7, max_length=100, example="john.doe@example.com")
    phone: str = Field(min_length=7, max_length=20, example="+380501234567")
    birthday: date = Field(example="1990-01-01")
    info: Optional[str] = Field(None, max_length=500, example="Additional info")

    # Валідація номера телефону
    @validator("phone")
    def validate_phone(cls, value):
        # Перевірка формату номера телефону (наприклад, +380501234567)
        phone_regex = r"^\+?[1-9]\d{1,14}$"  # Міжнародний формат
        if not re.match(phone_regex, value):
            raise ValueError("Phone number must be in international format (e.g., +380501234567)")
        return value

    # Валідація дня народження
    @validator("birthday")
    def validate_birthday(cls, value):
        # Перевірка, що дата народження не в майбутньому
        if value > date.today():
            raise ValueError("Birthday cannot be in the future")
        return value

class ContactResponse(ContactModel):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)  # Підтримка ORM mode