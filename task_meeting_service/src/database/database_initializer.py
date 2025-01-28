async def create_tables(db):
    async with db.get_session() as conn:
        # Таблица projects
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id SERIAL PRIMARY KEY,
                project_name VARCHAR(100) UNIQUE NOT NULL,
                project_oid VARCHAR(50) UNIQUE NOT NULL,
                status VARCHAR(20) NOT NULL,
                description TEXT,
                release_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Таблица users
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                user_oid VARCHAR(50) UNIQUE NOT NULL,
                user_name VARCHAR(100) NOT NULL,
                user_email VARCHAR(100) NOT NULL,
                user_role VARCHAR(50),
                project_oid VARCHAR(50) REFERENCES projects(project_oid) ON DELETE SET NULL
            );
        """)

        # Таблица tasks
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                description TEXT NOT NULL,
                status VARCHAR(20) NOT NULL,
                project_oid VARCHAR(50) NOT NULL REFERENCES projects(project_oid) ON DELETE CASCADE,
                user_name VARCHAR(100),
                status_changed_at TIMESTAMP,
                deadline TIMESTAMP
            );
        """)

        # Таблица team
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS team (
                id SERIAL PRIMARY KEY,
                team_oid VARCHAR(50) UNIQUE NOT NULL,
                team_name VARCHAR(100) NOT NULL,
                project_oid VARCHAR(50) NOT NULL REFERENCES projects(project_oid) ON DELETE CASCADE,
                user_oid VARCHAR(50) NOT NULL REFERENCES users(user_oid) ON DELETE CASCADE
            );
        """)