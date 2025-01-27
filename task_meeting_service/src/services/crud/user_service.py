class UserService:
    def __init__(self, db):
        self.db = db

    async def create_user(self, user_data):
        query = """
            INSERT INTO users (user_oid, user_name, user_email, user_role, project_id)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (user_oid) DO NOTHING;
        """
        async with self.db.get_session() as conn:
            await conn.execute(
                query,
                user_data.user_oid,
                user_data.user_name,
                user_data.user_email,
                user_data.user_role,
                user_data.project_id,
            )

    async def get_user(self, user_oid):
        query = "SELECT * FROM users WHERE user_oid = $1;"
        async with self.db.get_session() as conn:
            return await conn.fetchrow(query, user_oid)

    async def delete_user(self, user_oid):
        query = "DELETE FROM users WHERE user_oid = $1;"
        async with self.db.get_session() as conn:
            await conn.execute(query, user_oid)

    async def update_user(self, user_oid, updates: dict):
        fields = ", ".join(f"{key} = ${idx + 2}" for idx, key in enumerate(updates.keys()))
        query = f"""
            UPDATE users
            SET {fields}
            WHERE user_oid = $1
        """
        async with self.db.get_session() as conn:
            await conn.execute(query, user_oid, *updates.values())
