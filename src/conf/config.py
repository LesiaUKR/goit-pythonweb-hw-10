from pydantic_settings import BaseSettings  # Оновлений імпорт

class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str

    @property
    def database_url(self) -> str:
        """Формує URL для підключення до PostgreSQL."""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"  # Вказуємо, що змінні середовища беруться з .env файлу

settings = Settings()