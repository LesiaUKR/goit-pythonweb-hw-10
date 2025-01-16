from sqlalchemy import Integer, String, DateTime, Date, Column, func, Boolean,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20), nullable=False, unique=True)
    birthday = Column(Date, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    info = Column(String(500), nullable=True)
    # Додаємо зовнішній ключ для зв'язку з таблицею users
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # Встановлюємо зв'язок з моделлю User
    user = relationship("User", back_populates="contacts")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    is_verified = Column(Boolean, default=False)
    avatar_url = Column(String(255), nullable=True)
    # Встановлюємо зв'язок з моделлю Contact
    contacts = relationship("Contact", back_populates="user")