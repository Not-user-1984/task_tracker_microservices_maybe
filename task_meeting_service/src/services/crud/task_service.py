class TaskService:
    def __init__(self, db):
        self.db = db

    async def create_task(self, task_data):
        query = """
            INSERT INTO tasks (description, status, project_oid, user_name, status_changed_at, deadline)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id;
        """
        async with self.db.get_session() as conn:
            result = await conn.fetchrow(
                query,
                task_data["description"],
                task_data["status"],
                str(task_data["project_oid"]),
                task_data["user_name"],
                task_data["status_changed_at"],
                task_data["deadline"],
            )
            return result["id"]

    async def get_task(self, project_oid):
        query = """
            SELECT * FROM tasks
            WHERE project_oid = $1;
        """
        async with self.db.get_session() as conn:
            return await conn.fetchrow(query, project_oid)

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
