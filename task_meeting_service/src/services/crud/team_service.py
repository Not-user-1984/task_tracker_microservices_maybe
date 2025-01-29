from typing import Dict, List


class TeamService:
    def __init__(self, db):
        self.db = db

    async def create_team(self, team_data):
        query = """
            INSERT INTO team (team_oid, team_name, project_oid, user_oid)
            VALUES ($1, $2, $3, $4)
            RETURNING *;
        """
        async with self.db.get_session() as conn:
            result = await conn.fetchrow(
                query,
                team_data.team_oid,
                team_data.team_name,
                team_data.project_oid,
                team_data.user_oid,
            )
            return dict(result)

    async def get_team_by_oid(self, team_oid: str):
        query = "SELECT * FROM team WHERE team_oid = $1;"
        async with self.db.get_session() as conn:
            result = await conn.fetchrow(query, team_oid)
            if result:
                return dict(result)
            return None

    async def get_teams_by_project(self, project_oid: str) -> List[Dict]:
        query = "SELECT * FROM team WHERE project_oid = $1;"
        async with self.db.get_session() as conn:
            results = await conn.fetch(query, project_oid)
            return [dict(row) for row in results]

    async def update_team(self,team_data):
        query = """
            UPDATE team
            SET team_name = $1, project_oid = $2, user_oid = $3
            WHERE team_oid = $4
            RETURNING id;
        """
        async with self.db.get_session() as conn:
            result = await conn.fetchrow(
                query,
                team_data.team_name,
                team_data.project_oid,
                team_data.user_oid,
                team_data.team_oid,
            )
            if result:
                return dict(result)
            else:
                raise ValueError(f"Команда с team_oid {team_data.team_oid} не найдена.")

    async def delete_team(self, team_oid: str):
        query = "DELETE FROM team WHERE team_oid = $1 RETURNING id;"
        async with self.db.get_session() as conn:
            result = await conn.fetchrow(query, team_oid)
            if result:
                return dict(result)
            else:
                raise ValueError(f"Команда с team_oid {team_oid} не найдена.")

    async def create_or_update_user_project_role(self, user_assignment):
        """
        Создаёт или обновляет связь между пользователем, проектом и программой.
        """
        query = """
            INSERT INTO user_project_roles (user_oid, project_oid, program_name, role)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (user_oid, project_oid, program_name)
            DO UPDATE SET role = EXCLUDED.role;
        """
        async with self.db.get_session() as conn:
            await conn.execute(
                query,
                user_assignment.user_oid,
                user_assignment.project_oid,
                user_assignment.project_name,
                user_assignment.user_role,
            )
