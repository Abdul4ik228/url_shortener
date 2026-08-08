from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from .config import settings

#Создаем асинхронный движок для работы с PostgreSQL
#echo=True - включает логирование SQL запросов

engine = create_async_engine(settings.DATABASE_URL, echo=True)

#Создаем фабрику сессий
#expire_on_commit=False - отключает автоматическое закрытие сессий после выполнения запроса

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

#Базовый класс для моделей (таблиц)
Base = declarative_base()

#Функция для получения сессии в эндпоинтах
async def get_db():

    """Dependency для FastAPI. Создает сессию БД, отдает ее в эндпоинты, 
    и автоматически закрывает после завершения запроса. """

    async with AsyncSessionLocal() as session:
        yield session