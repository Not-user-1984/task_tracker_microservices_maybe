import pytest
import pytest_asyncio
import uuid
from datetime import date, timedelta
from src.services.crud.task_service import TaskService
from src.schemas.api.task import (
    TaskCreateSchema,
)


def generate_unique_project():
    unique_suffix = uuid.uuid4().hex[:6]
    project_oid = f"proj_{unique_suffix}"
    project_name = f"Test Project {unique_suffix}"
    return project_oid, project_name


def generate_unique_user():
    return f"user_{uuid.uuid4().hex[:6]}"


@pytest.mark.asyncio
async def test_create_task(test_db):
    """
    Тест создания задачи.
    """
    task_service = TaskService(test_db)

    project_oid, project_name = generate_unique_project()
    user_oid = generate_unique_user()

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
            INSERT INTO users (user_oid, user_name, user_email, user_role, project_oid)
            VALUES ($1, $2, $3, $4, $5)
            """,
            user_oid,
            "Test User",
            "test@example.com",
            "user",
            project_oid,
        )

    now = date.today()
    deadline = now + timedelta(days=7)
    task_data = TaskCreateSchema(
        description="Test task",
        status="new",
        deadline=deadline,
        project_oid=project_oid,
        user_oid=user_oid,
        status_changed_at=now,
    )

    result = await task_service.create_task(task_data)
    assert result is not None
    task_id = result.get("id")
    assert task_id is not None

    async with test_db.get_session() as conn:
        task = await conn.fetchrow("SELECT * FROM tasks WHERE id = $1", task_id)
    assert task is not None
    assert task["description"] == "Test task"
    assert task["status"] == "new"
    assert task["project_oid"] == project_oid
    assert task["user_oid"] == user_oid


@pytest.mark.asyncio
async def test_get_task(test_db):
    """
    Тест получения задачи по project_oid.
    """
    task_service = TaskService(test_db)

    project_oid, project_name = generate_unique_project()
    user_oid = generate_unique_user()
    now = date.today()
    deadline = now + timedelta(days=7)

    async with test_db.get_session() as conn:
        # Вставляем проект
        await conn.execute(
            """
            INSERT INTO projects (project_oid, project_name, status)
            VALUES ($1, $2, 'active')
            """,
            project_oid,
            project_name,
        )
        # Вставляем пользователя
        await conn.execute(
            """
            INSERT INTO users (user_oid, user_name, user_email, user_role, project_oid)
            VALUES ($1, $2, $3, $4, $5)
            """,
            user_oid,
            "Test User",
            "test@example.com",
            "user",
            project_oid,
        )
        # Вставляем задачу
        await conn.execute(
            """
            INSERT INTO tasks (description, status, project_oid, user_oid, status_changed_at, deadline)
            VALUES ($1, $2, $3, $4, $5, $6)
            """,
            "Get task test",
            "in progress",
            project_oid,
            user_oid,
            now,
            deadline,
        )

    task = await task_service.get_task(project_oid)
    assert task is not None
    assert task["description"] == "Get task test"
    assert task["status"] == "in progress"


@pytest.mark.asyncio
async def test_get_task_by_id(test_db):
    """
    Тест получения задачи по её id.
    """
    task_service = TaskService(test_db)

    project_oid, project_name = generate_unique_project()
    user_oid = generate_unique_user()
    now = date.today()
    deadline = now + timedelta(days=7)

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
            INSERT INTO users (user_oid, user_name, user_email, user_role, project_oid)
            VALUES ($1, $2, $3, $4, $5)
            """,
            user_oid,
            "Test User",
            "test@example.com",
            "user",
            project_oid,
        )
        result = await conn.fetchrow(
            """
            INSERT INTO tasks (description, status, project_oid, user_oid, status_changed_at, deadline)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id;
            """,
            "Task by id",
            "done",
            project_oid,
            user_oid,
            now,
            deadline,
        )
    task_id = result.get("id")
    task = await task_service.get_task_by_id(task_id)
    assert task is not None
    assert task["description"] == "Task by id"
    assert task["status"] == "done"


@pytest.mark.asyncio
async def test_get_tasks(test_db):
    """
    Тест получения списка задач с фильтрацией по project_oid и user_oid.
    """
    task_service = TaskService(test_db)

    project_oid, project_name = generate_unique_project()
    now = date.today()
    deadline = now + timedelta(days=7)
    user_oid1 = generate_unique_user()
    user_oid2 = generate_unique_user()

    async with test_db.get_session() as conn:
        # Вставляем проект
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
            INSERT INTO users (user_oid, user_name, user_email, user_role, project_oid)
            VALUES ($1, $2, $3, $4, $5)
            """,
            user_oid1,
            "User One",
            "one@example.com",
            "user",
            project_oid,
        )
        await conn.execute(
            """
            INSERT INTO users (user_oid, user_name, user_email, user_role, project_oid)
            VALUES ($1, $2, $3, $4, $5)
            """,
            user_oid2,
            "User Two",
            "two@example.com",
            "user",
            project_oid,
        )
        await conn.execute(
            """
            INSERT INTO tasks (description, status, project_oid, user_oid, status_changed_at, deadline)
            VALUES ($1, $2, $3, $4, $5, $6)
            """,
            "Task A",
            "new",
            project_oid,
            user_oid1,
            now,
            deadline,
        )
        await conn.execute(
            """
            INSERT INTO tasks (description, status, project_oid, user_oid, status_changed_at, deadline)
            VALUES ($1, $2, $3, $4, $5, $6)
            """,
            "Task B",
            "new",
            project_oid,
            user_oid2,
            now,
            deadline,
        )

    tasks_by_project = await task_service.get_tasks(project_oid=project_oid)
    assert len(tasks_by_project) >= 2

    tasks_by_user = await task_service.get_tasks(user_oid=user_oid1)
    for task in tasks_by_user:
        assert task["user_oid"] == user_oid1


@pytest.mark.asyncio
async def test_update_task(test_db):
    """
    Тест обновления задачи.
    """
    task_service = TaskService(test_db)

    project_oid, project_name = generate_unique_project()
    user_oid = generate_unique_user()
    now = date.today()
    deadline = now + timedelta(days=7)

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
            INSERT INTO users (user_oid, user_name, user_email, user_role, project_oid)
            VALUES ($1, $2, $3, $4, $5)
            """,
            user_oid,
            "Test User",
            "test@example.com",
            "user",
            project_oid,
        )
        result = await conn.fetchrow(
            """
            INSERT INTO tasks (description, status, project_oid, user_oid, status_changed_at, deadline)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id;
            """,
            "Old task",
            "pending",
            project_oid,
            user_oid,
            now,
            deadline,
        )
    task_id = result.get("id")

    updated_data = TaskCreateSchema(
        description="Updated task",
        status="completed",
        deadline=deadline + timedelta(days=1),
        project_oid=project_oid,
        user_oid=user_oid,
        status_changed_at=now,
    )

    result = await task_service.update_task(task_id, updated_data)
    assert result is not None
    assert result["description"] == "Updated task"
    assert result["status"] == "completed"
    assert result["project_oid"] == project_oid
    assert result["user_oid"] == user_oid
    assert result["deadline"].date() == updated_data.deadline


async def delete_task(self, description: str, project_oid: str):
    query = "DELETE FROM tasks WHERE description = $1 AND project_oid = $2;"
    async with self.db.get_session() as conn:
        await conn.execute(query, description, project_oid)
