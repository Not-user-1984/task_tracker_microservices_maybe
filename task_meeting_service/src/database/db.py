import asyncpg
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

# from src.core.config import settings
postgres_url = "postgresql://task_user:task_password@db_task:5432/task"


class DatabaseSessionManager:
    """
    Менеджер для управления асинхронными сессиями базы данных.
    """

    def __init__(self):
        self.connection_pool: Optional[asyncpg.pool.Pool] = None

    async def connect(self):
        """
        Создает пул соединений с базой данных.
        """
        self.connection_pool = await asyncpg.create_pool(
            dsn=postgres_url, min_size=1, max_size=10, command_timeout=60
        )

    async def close(self):
        """
        Закрывает пул соединений с базой данных.
        """
        if self.connection_pool:
            await self.connection_pool.close()

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[asyncpg.Connection, None]:
        """
        Асинхронный контекстный менеджер для получения соединения с базой данных.
        """
        if not self.connection_pool:
            raise Exception("Пул соединений не инициализирован")

        async with self.connection_pool.acquire() as connection:
            try:
                yield connection
            finally:
                await self.connection_pool.release(connection)

    async def __aenter__(self) -> asyncpg.Connection:
        """
        Открывает новое соединение с базой данных.
        """
        if not self.connection_pool:
            raise Exception("Пул соединений не инициализирован")

        self.connection = await self.connection_pool.acquire()
        return self.connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Закрывает соединение с базой данных, выполняя commit или rollback в зависимости от наличия ошибок.
        """
        if exc_type:
            await self.connection.rollback()
        else:
            await self.connection.commit()

        await self.connection_pool.release(self.connection)


db_manager = DatabaseSessionManager()
