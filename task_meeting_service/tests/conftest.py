import asyncio
import pytest
import pytest_asyncio
from contextlib import asynccontextmanager
from src.database.db import db_manager
from src.database.database_initializer import create_test_schema, delete_all_data


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_db():
    """
    Фикстура, которая подключается к БД, создает тестовую схему,
    а по завершении сессии закрывает соединение.
    """
    await db_manager.connect()
    await create_test_schema(db_manager, schema="test")
    yield db_manager
    await db_manager.close()


@asynccontextmanager
async def dummy_get_session(conn):
    yield conn


@pytest_asyncio.fixture(autouse=True)
async def db_transaction(test_db):
    """
    Фикстура для оборачивания каждого теста в транзакцию.
    После теста транзакция откатывается – изменения не сохраняются в БД.
    Также устанавливается search_path в тестовую схему.
    """
    conn = await test_db.connection_pool.acquire()
    await conn.execute("SET search_path TO test;")
    transaction = conn.transaction()
    await transaction.start()

    original_get_session = test_db.get_session
    test_db.get_session = lambda: dummy_get_session(conn)

    try:
        yield
    finally:
        await transaction.rollback()
        test_db.get_session = original_get_session
        await test_db.connection_pool.release(conn)


@pytest_asyncio.fixture(autouse=True)
async def cleanup_test_data(test_db):
    await delete_all_data(test_db, schema="test")
