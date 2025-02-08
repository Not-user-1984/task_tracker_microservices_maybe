from typing import Optional
from pydantic import BaseModel
from src.schemas.api.task import TaskUpdateSchema


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
                task_data.description,
                task_data.status,
                task_data.project_oid,
                task_data.user_oid,
                task_data.status_changed_at,
                task_data.deadline,
            )
            return result

    async def get_task(self, project_oid):
        query = """
            SELECT * FROM tasks
            WHERE project_oid = $1;
        """
        async with self.db.get_session() as conn:
            return await conn.fetchrow(query, project_oid)

    async def delete_task(self, description: str, project_oid: str):
        query = "DELETE FROM tasks WHERE description = $1 AND project_oid = $2;"
        async with self.db.get_session() as conn:
            await conn.execute(query, description, project_oid)

    async def get_task_by_id(self, task_id: int):
        query = """
            SELECT * FROM tasks
            WHERE id = $1;
        """
        async with self.db.get_session() as conn:
            return await conn.fetchrow(query, task_id)

    async def update_task(self, task_id: int, task: TaskUpdateSchema):
        query = """
            UPDATE tasks

            SET description = $1,
                status = $2,
                project_oid = $3,
                user_oid = $4,
                status_changed_at = $5,
                deadline = $6
            WHERE id = $7
            RETURNING id, description, status, deadline, project_oid, user_oid, status_changed_at;
        """

        async with self.db.get_session() as conn:
            result = await conn.fetchrow(
                query,
                task.description,
                task.status,
                task.project_oid,
                task.user_oid,
                task.status_changed_at,
                task.deadline,
                task_id,
            )
            return result

    async def get_tasks(
        self, project_oid: Optional[str] = None, user_oid: Optional[str] = None
    ):
        query = "SELECT * FROM tasks"
        params = []
        conditions = []

        if project_oid:
            conditions.append("project_oid = $" + str(len(params) + 1))
            params.append(project_oid)
        if user_oid:
            conditions.append("user_oid = $" + str(len(params) + 1))
            params.append(user_oid)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        async with self.db.get_session() as conn:
            return await conn.fetch(query, *params)
