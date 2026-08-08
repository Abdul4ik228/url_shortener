from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    """Класс для хранения всех настроек приложения. Автоматом читает переменные из файла .env"""

    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5433/url_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_SALT: str = "my_super_secret_salt_2026"
    BASE_DOMAIN: str = "http://localhost:8000"
    REDIS_TTL: int = 3600

    class Config:
        env_file = ".env"

# Создаем один экземпляр класса Settings для доступа к настройкам из других модулей
settings = Settings()
