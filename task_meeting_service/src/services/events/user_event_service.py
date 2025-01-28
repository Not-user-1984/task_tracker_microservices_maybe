from typing import Any, Dict, Callable
from src.services.crud.user_service import UserService
from src.services.crud.project_service import ProjectService
from src.services.crud.task_service import TaskService
from src.services.crud.team_service import TeamService
from src.schemas.user_events import UserEventSchemas


class UserEventService:
    def __init__(self, logger, db):
        self.logger = logger
        self.user_service = UserService(db)
        self.project_service = ProjectService(db)
        self.task_service = TaskService(db)
        self.teams_service = TeamService(db)

    async def handle_creation(self, user_assignment: UserEventSchemas):
        """
        Обрабатывает создание проекта, пользователя и команды.
        """
        try:
            # Создание проекта
            await self._handle_entity(
                entity_oid=user_assignment.project_oid,
                get_method=self.project_service.get_project_by_oid,
                create_method=self.project_service.create_project,
                entity_name="проект",
                entity_data=user_assignment,
                log_name=user_assignment.project_name,
            )

            # Создание пользователя
            await self._handle_entity(
                entity_oid=user_assignment.user_oid,
                get_method=self.user_service.get_user,
                create_method=self.user_service.create_user,
                entity_name="пользователь",
                entity_data=user_assignment,
                log_name=user_assignment.user_name,
            )

            # Создание команды
            await self._handle_entity(
                entity_oid=user_assignment.team_oid,
                get_method=self.teams_service.get_team_by_oid,
                create_method=self.teams_service.create_team,
                entity_name="команда",
                entity_data=user_assignment,
                log_name=user_assignment.team_name,
            )

        except Exception as e:
            self.logger.error(f"Ошибка при обработке создания: {e}")
            raise

    async def handle_deletion(self, key: Dict[str, Any]):
        """
        Обрабатывает удаление задач, проектов, пользователей и команд.
        """
        try:
            if "description" in key and "project_id" in key:
                await self.task_service.delete_task(key["description"], key["project_id"])
                self.logger.info(
                    f"Удалена задача: {key['description']} из проекта {key['project_id']}"
                )

            if "project_name" in key:
                await self.project_service.delete_project(key["project_name"])
                self.logger.info(f"Удален проект: {key['project_name']}")

            if "user_oid" in key:
                await self.user_service.delete_user(key["user_oid"])
                self.logger.info(f"Удален пользователь: {key['user_oid']}")

            if "team_oid" in key:
                await self.teams_service.delete_team(key["team_oid"])
                self.logger.info(f"Удалена команда: {key['team_oid']}")

        except Exception as e:
            self.logger.error(f"Ошибка при обработке удаления: {e}")
            raise

    async def handle_update(self, user_assignment: UserEventSchemas):
        """
        Обрабатывает обновление или создание проекта, пользователя и команды.
        """
        try:
            # Обновление или создание проекта
            await self._handle_entity(
                entity_oid=user_assignment.project_oid,
                get_method=self.project_service.get_project_by_oid,
                update_method=self.project_service.update_project,
                create_method=self.project_service.create_project,
                entity_name="проект",
                entity_data=user_assignment,
                log_name=user_assignment.project_name,
            )

            # Обновление или создание пользователя
            await self._handle_entity(
                entity_oid=user_assignment.user_oid,
                get_method=self.user_service.get_user,
                update_method=self.user_service.update_user,
                create_method=self.user_service.create_user,
                entity_name="пользователь",
                entity_data=user_assignment,
                log_name=user_assignment.user_name,
            )

            # Обновление или создание команды
            await self._handle_entity(
                entity_oid=user_assignment.team_oid,
                get_method=self.teams_service.get_team_by_oid,
                update_method=self.teams_service.update_team,
                create_method=self.teams_service.create_team,
                entity_name="команда",
                entity_data=user_assignment,
                log_name=user_assignment.team_name,
            )

        except Exception as e:
            self.logger.error(f"Ошибка при обработке обновления: {e}")
            raise

    async def _handle_entity(
        self,
        entity_oid: int,
        get_method: Callable,
        update_method: Callable = None,
        create_method: Callable = None,
        entity_name: str = "",
        entity_data: UserEventSchemas = None,

        log_name: str = "",
    ):
        """
        Универсальный метод для обработки обновления или создания сущности.

        :param entity_oid: Уникальный идентификатор сущности.
        :param get_method: Метод для получения сущности.
        :param update_method: Метод для обновления сущности.
        :param create_method: Метод для создания сущности.
        :param entity_name: Название сущности (для логов).
        :param entity_data: Данные для обновления или создания.
        :param log_name: Название сущности для логирования.
        """
        entity = await get_method(entity_oid)

        if entity:
            if update_method:
                await update_method(entity_data)
                self.logger.info(f"Обновлен {entity_name}: {log_name}")
        else:
            if create_method:
                await create_method(entity_data)
                self.logger.info(f"Создан новый {entity_name}: {log_name}")
