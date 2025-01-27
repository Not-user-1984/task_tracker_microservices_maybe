class TaskService:
    def __init__(self, db):
        self.db = db

    async def create_task(self, task_data):
        query = """
            INSERT INTO tasks (description, status, project_id, user_name, status_changed_at, deadline)
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT DO NOTHING;
        """
        async with self.db.get_session() as conn:
            await conn.execute(
                query,
                task_data["description"],
                task_data["status"],
                task_data["project_id"],
                task_data["user_name"],
                task_data["status_changed_at"],
                task_data["deadline"],
            )

    async def get_task(self, description, project_id):
        query = "SELECT * FROM tasks WHERE description = $1 AND project_id = $2;"
        async with self.db.get_session() as conn:
            return await conn.fetchrow(query, description, project_id)

    async def delete_task(self, description, project_id):
        query = "DELETE FROM tasks WHERE description = $1 AND project_id = $2;"
        async with self.db.get_session() as conn:
            await conn.execute(query, description, project_id)

    async def update_task(self, description, project_id, updates: dict):
        fields = ", ".join(
            f"{key} = ${idx + 3}" for idx, key in enumerate(updates.keys())
        )
        query = f"""
            UPDATE tasks
            SET {fields}
            WHERE description = $1 AND project_id = $2
        """
        async with self.db.get_session() as conn:
            await conn.execute(query, description, project_id, *updates.values())
