import asyncpg
from src.core.config import settings

SCHEMA_TEST = settings.SCHEMA_TEST
SCHEMA_SERVICE = settings.SCHEMA_SERVICE
ALLOWED_SCHEMAS = settings.get_allowed_schemas()


# PostgreSQL не поддерживает параметризацию в DDL-запросах
def validate_schema_name(schema: str) -> bool:
    """
    Проверяет, что имя схемы разрешено.
    """
    return schema in ALLOWED_SCHEMAS


async def create_tables(db, schema: str = SCHEMA_SERVICE):
    """
    Создает таблицы в указанной схеме.
    По умолчанию используется схема public.
    """
    if not validate_schema_name(schema):
        raise ValueError(f"Схема '{schema}' не разрешена.")

    async with db.get_session() as conn:
        if schema != SCHEMA_SERVICE:
            await conn.execute(f"SET search_path TO {schema};")

        # Таблица projects
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id SERIAL PRIMARY KEY,
                project_name VARCHAR(100) UNIQUE NOT NULL,
                project_oid VARCHAR(50) UNIQUE NOT NULL,
                status VARCHAR(20) NOT NULL,
                description TEXT,
                release_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        )

        # Таблица users
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                user_oid VARCHAR(50) UNIQUE NOT NULL,
                user_name VARCHAR(100) NOT NULL,
                user_email VARCHAR(100) NOT NULL,
                user_role VARCHAR(50),
                is_deleted BOOLEAN DEFAULT FALSE,
                project_oid VARCHAR(50) REFERENCES projects(project_oid) ON DELETE SET NULL
            );
        """
        )

        # Таблица tasks
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                description TEXT NOT NULL,
                status VARCHAR(20) NOT NULL,
                project_oid VARCHAR(50) NOT NULL REFERENCES projects(project_oid) ON DELETE CASCADE,
                user_oid VARCHAR(50) REFERENCES users(user_oid) ON DELETE SET NULL,
                status_changed_at TIMESTAMP,
                deadline TIMESTAMP
            );
        """
        )

        # Таблица team
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS team (
                id SERIAL PRIMARY KEY,
                team_oid VARCHAR(50) UNIQUE NOT NULL,
                team_name VARCHAR(100) NOT NULL,
                project_oid VARCHAR(50) NOT NULL REFERENCES projects(project_oid) ON DELETE CASCADE,
                user_oid VARCHAR(50) NOT NULL REFERENCES users(user_oid) ON DELETE CASCADE
            );
        """
        )

        # Таблица user_project_roles
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user_project_roles (
                id SERIAL PRIMARY KEY,
                user_oid VARCHAR(50) NOT NULL REFERENCES users(user_oid) ON DELETE CASCADE,
                project_oid VARCHAR(50) NOT NULL REFERENCES projects(project_oid) ON DELETE CASCADE,
                program_name VARCHAR(100),
                role VARCHAR(50),
                UNIQUE (user_oid, project_oid, program_name)
            );
        """
        )


async def delete_all_data(db, schema: str = SCHEMA_SERVICE):
    """
    Удаляет все данные из таблиц в указанной схеме.
    Используется TRUNCATE с RESTART IDENTITY для сброса счетчиков.
    """
    if not validate_schema_name(schema):
        raise ValueError(f"Схема '{schema}' не разрешена.")

    async with db.get_session() as conn:
        if schema != SCHEMA_SERVICE:
            await conn.execute(f"SET search_path TO {schema};")
        await conn.execute(
            "TRUNCATE TABLE user_project_roles RESTART IDENTITY CASCADE;"
        )
        await conn.execute("TRUNCATE TABLE team RESTART IDENTITY CASCADE;")
        await conn.execute("TRUNCATE TABLE tasks RESTART IDENTITY CASCADE;")
        await conn.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE;")
        await conn.execute("TRUNCATE TABLE projects RESTART IDENTITY CASCADE;")


async def create_test_schema(db, schema: str = SCHEMA_TEST):
    """
    Создает отдельную схему (по умолчанию test) в текущей БД.
    Если схема уже существует, она удаляется вместе со всеми объектами (CASCADE),
    затем создается заново и в ней создаются таблицы.
    """
    if not validate_schema_name(schema):
        raise ValueError(f"Схема '{schema}' не разрешена.")

    async with db.get_session() as conn:
        await conn.execute(f"DROP SCHEMA IF EXISTS {schema} CASCADE;")
        await conn.execute(f"CREATE SCHEMA {schema};")
    await create_tables(db, schema)
