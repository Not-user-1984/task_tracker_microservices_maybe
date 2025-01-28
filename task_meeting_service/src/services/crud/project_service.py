from typing import Dict
from src.schemas.user_events import UserEventSchemas

class ProjectService:
    def __init__(self, db):
        self.db = db

    async def create_project(self, project_data):
        query = """
            INSERT INTO projects (project_name, project_oid, status)
            VALUES ($1, $2, $3)
            RETURNING *;
        """
        async with self.db.get_session() as conn:
            result = await conn.fetchrow(
                query,
                project_data.project_name,
                project_data.project_oid,
                'create',
            )
            return dict(result)

    async def get_project(self, project_name):
        query = """
            SELECT * FROM projects
            WHERE project_name = $1;
        """
        async with self.db.get_session() as conn:
            result = await conn.fetchrow(query, project_name)
            if result:
                return dict(result)
            return None

    async def get_project_by_oid(self, project_oid: str):
        query = "SELECT * FROM projects WHERE project_oid = $1;"
        async with self.db.get_session() as conn:
            return await conn.fetchrow(query, project_oid)

    async def update_project(self, project_data: UserEventSchemas):
        async with self.db.get_session() as session:
            query = """
                UPDATE projects
                SET project_name = $1, project_oid = $2, status = $3
                WHERE project_oid = $4
                RETURNING id;
            """
            values = (
                project_data.project_name,
                project_data.project_oid,
                'update',
                project_data.project_oid,
            )

            result = await session.fetch(query, *values)

            if result:
                return result[0]["id"]
            else:
                raise ValueError(f"Проект с id {project_data.project_oidect_oid} не найден.")
