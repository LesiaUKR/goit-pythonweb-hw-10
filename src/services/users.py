from fastapi import HTTPException, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from src.repository.users import UserRepository
from src.schemas import UserCreate, User
from src.services.uploadfile import UploadFileService
from src.conf.config import settings


class UserService:
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def create_user(self, body: UserCreate) -> User:
        """
        Створення нового користувача.
        Перевіряє, чи існує користувач з таким email або username.
        """
        # Перевірка наявності користувача з таким email
        if await self.repository.get_user_by_email(body.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )
        # Перевірка наявності користувача з таким username
        if await self.repository.get_user_by_username(body.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this username already exists",
            )
        # Створення користувача в базі даних
        return await self.repository.create_user(body.dict())

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Отримання користувача за ID.
        """
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Отримання користувача за іменем користувача.
        """
        user = await self.repository.get_user_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Отримання користувача за електронною поштою.
        """
        user = await self.repository.get_user_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    async def update_avatar(self, user_id: int, file: UploadFile) -> User:
        """
        Оновлення аватара користувача.
        Завантажує файл на Cloudinary та оновлює URL аватара в базі даних.
        """
        # Ініціалізація сервісу для завантаження файлів
        upload_service = UploadFileService(
            settings.CLOUDINARY_CLOUD_NAME,
            settings.CLOUDINARY_API_KEY,
            settings.CLOUDINARY_API_SECRET,
        )
        # Завантаження файлу на Cloudinary
        avatar_url = await upload_service.upload_file(file, f"user_{user_id}")
        # Оновлення URL аватара в базі даних
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        updated_user = await self.repository.update_avatar_url(user.email, avatar_url)
        return updated_user

    async def verify_email(self, email: str) -> None:
        """
        Підтвердження email користувача.
        """
        user = await self.repository.get_user_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        await self.repository.confirmed_email(email)