from src.schemas.user_events import UserEventSchemas


class UserService:
    def __init__(self, db):
        self.db = db

    async def create_user(self, user_data: UserEventSchemas):
        """
        Создает нового пользователя в базе данных.

        :param user_data: Объект UserEventSchemas с данными пользователя.
        :return: ID созданного пользователя.
        """
        query = """
            INSERT INTO users (user_oid, user_name, user_email, user_role, project_oid)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id;
        """
        async with self.db.get_session() as conn:
            result = await conn.fetchrow(
                query,
                user_data.user_oid,  # Используем точечную нотацию
                user_data.user_name,
                user_data.user_email,
                user_data.user_role,
                user_data.project_oid,
            )
            return result["id"]

    async def update_user(self, user_data: UserEventSchemas):
        """
        Обновляет данные пользователя.

        :param user_oid: Уникальный идентификатор пользователя.
        :param user_data: Объект UserEventSchemas с обновленными данными пользователя.
        :return: ID обновленного пользователя.
        """
        query = """
            UPDATE users
            SET user_name = $1, user_email = $2, user_role = $3, project_oid = $4
            WHERE user_oid = $5
            RETURNING id;
        """
        async with self.db.get_session() as conn:
            result = await conn.fetchrow(
                query,
                user_data.user_name,
                user_data.user_email,
                user_data.user_role,
                user_data.project_oid,
                user_data.user_oid,
            )
            return result

    async def get_user(self, user_oid):
        """
        Получает данные пользователя по его user_oid.

        :param user_oid: Уникальный идентификатор пользователя.
        :return: Данные пользователя или None, если пользователь не найден.
        """
        query = "SELECT * FROM users WHERE user_oid = $1;"
        async with self.db.get_session() as conn:
            return await conn.fetchrow(query, user_oid)

    async def delete_user(self, user_oid):
        """
        Удаляет пользователя по его user_oid.

        :param user_oid: Уникальный идентификатор пользователя.
        """
        query = "DELETE FROM users WHERE user_oid = $1;"
        async with self.db.get_session() as conn:
            await conn.execute(query, user_oid)

    async def get_user_projects(self, user_oid: str):
        """
        Получает список проектов, связанных с пользователем.

        :param user_oid: Уникальный идентификатор пользователя.
        :return: Список проектов.
        """
        query = """
            SELECT p.*
            FROM projects p
            JOIN users u ON p.project_oid = u.project_oid
            WHERE u.user_oid = $1;
        """
        async with self.db.get_session() as conn:
            return await conn.fetch(query, user_oid)

    # async def update_user(self, user_oid, updates: dict):
    #     fields = ", ".join(
    #         f"{key} = ${idx + 2}" for idx, key in enumerate(updates.keys())
    #     )
    #     query = f"""
    #         UPDATE users
    #         SET {fields}
    #         WHERE user_oid = $1
    #     """
    #     async with self.db.get_session() as conn:
    #         await conn.execute(query, user_oid, *updates.values())
