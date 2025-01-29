from pydantic import BaseModel


class TaskService:
    def __init__(self, db):
        self.db = db

    async def create_task(self, task_data):
        query = """
            INSERT INTO tasks (description, status, project_oid, user_oid, status_changed_at, deadline)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id;
        """
        async with self.db.get_session() as conn:
            result = await conn.fetchrow(
                query,
                task_data["description"],
                task_data["status"],
                str(task_data["project_oid"]),
                task_data["user_oid"],
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

    # async def update_task(self, description, project_id, updates: dict):
    #     fields = ", ".join(
    #         f"{key} = ${idx + 3}" for idx, key in enumerate(updates.keys())
    #     )
    #     query = f"""
    #         UPDATE tasks
    #         SET {fields}
    #         WHERE description = $1 AND project_id = $2
    #     """
    #     async with self.db.get_session() as conn:
    #         await conn.execute(query, description, project_id, *updates.values())

    async def update_task(self, task_id: int, task: BaseModel):
        query = """
            UPDATE tasks
            SET description = $1,
                status = $2,
                project_oid = $3,
                user_oid = $4,
                status_changed_at = $5,
                deadline = $6
            WHERE id = $7
            RETURNING id;
        """

        # Подставляем значения из объекта task
        async with self.db.get_session() as conn:
            result = await conn.fetchrow(
                query,
                task.description,
                task.status,
                task.project_oid,
                task.user_oid,
                task.status_changed_at,
                task.deadline,
                task_id,  # Идентификатор задачи, которую обновляем
            )
            return result
