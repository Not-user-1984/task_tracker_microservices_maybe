from src.schemas.user_events import UserEventSchemas
from src.schemas.api.user import UserUpdateSchema


class UserService:
    def __init__(self, db):
        self.db = db

    async def update_user_by_oid(self, user_oid: str, data: UserUpdateSchema):
        """
        Обновляет project_oid пользователя по user_oid.

        :param user_oid: Уникальный идентификатор пользователя.
        :param project_oid: Новый project_oid (опционально).
        :return: ID обновленного пользователя.
        """
        if data.project_oid is None:
            raise ValueError("Не передано значение для обновления project_oid")

        query = """
            UPDATE users
            SET project_oid = $1
            WHERE user_oid = $2
            RETURNING *;
        """
        async with self.db.get_session() as conn:
            result = await conn.fetchrow(query, data.project_oid, user_oid)
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
