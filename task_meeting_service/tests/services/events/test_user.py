import pytest
import pytest_asyncio
import uuid
from src.services.events.crud.user import UserService
from src.schemas.user_events import UserEventSchemas


def generate_unique_project():
    unique_suffix = uuid.uuid4().hex[:6]
    project_oid = f"proj_{unique_suffix}"
    project_name = f"Test Project {unique_suffix}"
    return project_oid, project_name


@pytest.mark.asyncio
async def test_create_user(test_db):
    """
    Тест создания пользователя.
    """
    user_service = UserService(test_db)

    project_oid, project_name = generate_unique_project()
    async with test_db.get_session() as conn:
        await conn.execute(
            """
            INSERT INTO projects (project_oid, project_name, status) 
            VALUES ($1, $2, 'active')
            """,
            project_oid,
            project_name,
        )

    user_data = UserEventSchemas(
        id=1,
        project_id=1,
        user_id=1,
        user_oid="user_001",
        user_name="Alice",
        user_email="alice@example.com",
        user_role="admin",
        project_oid=project_oid,
    )

    user_id = await user_service.create_user(user_data)

    async with test_db.get_session() as conn:
        user = await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)

    assert user is not None
    assert user["user_oid"] == "user_001"
    assert user["user_name"] == "Alice"
    assert user["user_email"] == "alice@example.com"
    assert user["user_role"] == "admin"
    assert user["project_oid"] == project_oid


@pytest.mark.asyncio
async def test_get_user(test_db):
    """
    Тест получения пользователя по user_oid.
    """
    user_service = UserService(test_db)

    project_oid, project_name = generate_unique_project()
    async with test_db.get_session() as conn:
        await conn.execute(
            """
            INSERT INTO projects (project_oid, project_name, status) 
            VALUES ($1, $2, 'active')
            """,
            project_oid,
            project_name,
        )
        # Создаем тестового пользователя
        await conn.execute(
            """
            INSERT INTO users (id, user_oid, user_name, user_email, user_role, project_oid) 
            VALUES (2, 'user_002', 'Bob', 'bob@example.com', 'user', $1)
            """,
            project_oid,
        )

    user = await user_service.get_user("user_002")

    assert user is not None
    assert user["user_oid"] == "user_002"
    assert user["user_name"] == "Bob"
    assert user["user_email"] == "bob@example.com"
    assert user["user_role"] == "user"


@pytest.mark.asyncio
async def test_update_user(test_db):
    """
    Тест обновления пользователя.
    """
    user_service = UserService(test_db)

    project_oid, project_name = generate_unique_project()
    async with test_db.get_session() as conn:
        await conn.execute(
            """
            INSERT INTO projects (project_oid, project_name, status) 
            VALUES ($1, $2, 'active')
            """,
            project_oid,
            project_name,
        )
        await conn.execute(
            """
            INSERT INTO users (id, user_oid, user_name, user_email, user_role, project_oid) 
            VALUES (3, 'user_003', 'Charlie', 'charlie@example.com', 'editor', $1)
            """,
            project_oid,
        )

    updated_data = UserEventSchemas(
        id=3,
        project_id=3,
        user_id=3,
        user_oid="user_003",
        user_name="Charlie Updated",
        user_email="charlie_new@example.com",
        user_role="admin",
        project_oid=project_oid,
    )

    await user_service.update_user(updated_data)

    async with test_db.get_session() as conn:
        user = await conn.fetchrow(
            "SELECT * FROM users WHERE user_oid = $1", "user_003"
        )

    assert user is not None
    assert user["user_name"] == "Charlie Updated"
    assert user["user_email"] == "charlie_new@example.com"
    assert user["user_role"] == "admin"


@pytest.mark.asyncio
async def test_delete_user(test_db):
    """
    Тест мягкого удаления пользователя.
    """
    user_service = UserService(test_db)

    project_oid, project_name = generate_unique_project()
    async with test_db.get_session() as conn:
        await conn.execute(
            """
            INSERT INTO projects (project_oid, project_name, status) 
            VALUES ($1, $2, 'active')
            """,
            project_oid,
            project_name,
        )
        await conn.execute(
            """
            INSERT INTO users (id, user_oid, user_name, user_email, user_role, project_oid, is_deleted) 
            VALUES (4, 'user_004', 'David', 'david@example.com', 'manager', $1, FALSE)
            """,
            project_oid,
        )

    await user_service.delete_user(4)

    async with test_db.get_session() as conn:
        user = await conn.fetchrow("SELECT is_deleted FROM users WHERE id = $1", 4)

    assert user is not None
    assert user["is_deleted"] is True


@pytest.mark.asyncio
async def test_get_user_projects(test_db):
    """
    Тест получения списка проектов пользователя.
    """
    user_service = UserService(test_db)

    project_oid, project_name = generate_unique_project()
    async with test_db.get_session() as conn:
        await conn.execute(
            """
            INSERT INTO projects (project_oid, project_name, status) 
            VALUES ($1, $2, 'active')
            """,
            project_oid,
            project_name,
        )
        await conn.execute(
            """
            INSERT INTO users (id, user_oid, user_name, user_email, user_role, project_oid) 
            VALUES (5, 'user_005', 'Eve', 'eve@example.com', 'user', $1)
            """,
            project_oid,
        )

    projects = await user_service.get_user_projects("user_005")
    assert len(projects) == 1
    assert projects[0]["project_oid"] == project_oid
    assert projects[0]["project_name"] == project_name
