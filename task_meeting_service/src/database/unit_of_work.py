from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from core.config import settings

# Создаем асинхронный движок для подключения к базе данных
engine = create_async_engine(settings.get_postgres_url(), echo=True)

# Создаем фабрику сессий
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Генератор для получения асинхронной сессии базы данных.
    """
    async with async_session() as session:
        yield session


class DatabaseSessionManager:
    """
    Менеджер для управления асинхронными сессиями базы данных.
    """

    def __init__(self):
        self.session_maker = async_session

    async def __aenter__(self) -> AsyncSession:
        """
        Открывает новую сессию базы данных.
        """
        self.session = self.session_maker()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Закрывает сессию базы данных, выполняя commit или rollback в зависимости от наличия ошибок.
        """
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()