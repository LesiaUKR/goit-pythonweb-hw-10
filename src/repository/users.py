from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database.models import User
from src.schemas import UserCreate

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: int) -> User | None:
        """
        Отримує користувача за ID.
        """
        stmt = select(User).filter(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        """
        Отримує користувача за іменем користувача.
        """
        stmt = select(User).filter(User.username == username)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Отримує користувача за електронною поштою.
        """
        stmt = select(User).filter(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, user: UserCreate, avatar_url: str = None) -> User:
        """
        Створює нового користувача.
        """
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=user.password,  # Пароль має бути хешований перед передачею
            avatar_url=avatar_url,  # Додаємо аватар, якщо він є
            is_verified=False,  # За замовчуванням користувач не підтверджений
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def confirmed_email(self, email: str) -> None:
        """
        Позначає електронну пошту користувача як підтверджену.
        """
        user = await self.get_user_by_email(email)
        if user:
            user.is_verified = True
            await self.db.commit()

    async def update_avatar_url(self, email: str, url: str) -> User:
        """
        Оновлює URL аватара користувача.
        """
        user = await self.get_user_by_email(email)
        if user:
            user.avatar_url = url
            await self.db.commit()
            await self.db.refresh(user)
        return user