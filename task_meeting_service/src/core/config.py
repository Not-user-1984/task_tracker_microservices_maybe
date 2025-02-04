from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    kafka_bootstrap_servers: str = "kafka:9092"
    kafka_topic: str = "django_db.public.teams_userassignment"
    kafka_group_id: str = "user-assignments-group"

    postgres_db: str = "task"
    postgres_user: str = "task_user"
    postgres_password: str = "task_password"
    postgres_host: str = "db_task"
    postgres_port: int = 5433

    SECRET_KEY = "ваш_секретный_ключ"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    class Config:
        env_file = ".env"

    def get_postgres_url(self) -> str:
        """
        Возвращает строку подключения к PostgreSQL.
        """
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
