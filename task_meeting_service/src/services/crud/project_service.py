class ProjectService:
    def __init__(self, db):
        self.db = db

    async def create_project(self, project_data):
        query = """
            INSERT INTO projects (project_name, status, description, release_date)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (project_name) DO NOTHING;
        """
        async with self.db.get_session() as conn:
            await conn.execute(
                query,
                project_data.project_name,
                project_data.status,
                project_data.description,
                project_data.release_date,
            )

    async def get_project(self, project_name):
        query = "SELECT * FROM projects WHERE project_name = $1;"
        async with self.db.get_session() as conn:
            return await conn.fetchrow(query, project_name)
