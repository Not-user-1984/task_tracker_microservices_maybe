import asyncpg
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

postgres_url = "postgresql://task_user:task_password@db_task:5432/task"

class DatabaseSessionManager:
    """
    Менеджер для управления асинхронными сессиями базы данных.
    """

    def __init__(self):
        self.connection_pool: Optional[asyncpg.pool.Pool] = None
        self.connection: Optional[asyncpg.Connection] = None

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

    def _raise_if_not_connected(self):
        """
        Выбрасывает исключение, если пул соединений не инициализирован.
        """
        if not self.connection_pool:
            raise Exception(
                "Пул соединений не инициализирован. Вызовите connect() перед использованием сессии."
            )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[asyncpg.Connection, None]:
        """
        Асинхронный контекстный менеджер для получения соединения с базой данных.
        """
        self._raise_if_not_connected()
        async with self.connection_pool.acquire() as connection:
            yield connection

    async def __aenter__(self) -> asyncpg.Connection:
        """
        Открывает новое соединение с базой данных.
        """
        self._raise_if_not_connected()

        if self.connection:
            await self.connection_pool.release(self.connection)

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
        self.connection = None

db_manager = DatabaseSessionManager()
