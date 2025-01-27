from typing import Dict


class ProjectService:
    def __init__(self, db):
        self.db = db

    async def create_project(self, project_data):
        query = """
            INSERT INTO projects (project_name, project_oid, status)
            VALUES ($1, $2, $3)
            ON CONFLICT (project_name) DO NOTHING;
        """
        async with self.db.get_session() as conn:
            await conn.execute(
                query,
                project_data.project_name,
                project_data.project_oid,
                project_data.status,
            )

    async def get_project(self, project_name):
        query = "SELECT * FROM projects WHERE project_name = $1;"
        async with self.db.get_session() as conn:
            return await conn.fetchrow(query, project_name)

    async def update_project(self, project_id: int, project_data: Dict):
        async with self.db.get_session() as session:
            query = """
                UPDATE projects
                SET project_name = $1, description = $2, status = $3, release_date = $4
                WHERE id = $5
                RETURNING id;
            """
            values = (
                project_data.get("project_name"),
                project_data.get("description"),
                project_data.get("status"),
                project_data.get("release_date"),
                project_id,
            )

            result = await session.fetch(query, *values)

            if result:
                return result[0]["id"]  # Возвращаем ID обновленного проекта
            else:
                raise ValueError(f"Проект с id {project_id} не найден.")
