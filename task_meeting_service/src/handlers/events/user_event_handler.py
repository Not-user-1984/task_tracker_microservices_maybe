import logging
from typing import Any, Dict, Set
from src.schemas.user_events import UserEventSchemas
from src.services.events.user_event_service import UserEventService
from src.database.db import DatabaseSessionManager

# from src.services.events.message_handler import MessageHandler


class UserEventHandler:
    def __init__(self, logger: logging.Logger, db_manager: DatabaseSessionManager):
        self.logger = logger
        self.user_event_service = UserEventService(logger, db_manager)

    async def handle_message(self, message: Dict[str, Any]) -> None:
        try:
            schema_fields = set(UserEventSchemas.__fields__.keys())
            extra_fields = self._find_extra_fields(message, schema_fields)

            if extra_fields:
                self.logger.warning(
                    f"Обнаружены поля, которых нет в схеме: {extra_fields}. "
                    f"Добавьте их в модель UserAssignmentSchema."
                )

            user_assignment = UserEventSchemas(**message)
            self.logger.info(f"Обработан объект: {user_assignment}")

            operation = message.get("__op")
            if operation == "c":
                self.logger.info(f"Создание обьекта: {user_assignment.user_oid}")
                await self.user_event_service.handle_creation(user_assignment)
            elif operation == "u":
                await self.user_event_service.handle_update(user_assignment)
                self.logger.info(f"обновление обьекта: {user_assignment.user_oid}")
        except Exception as e:
            self.logger.error(f"Ошибка обработки сообщения: {e}")

    async def handle_deletion(self, user_assignment):
        """
        Обра��атывает удаление объекта.
        """
        try:
            self.logger.info(f"Удаление обьекта: {user_assignment}")
            await self.user_event_service.handle_deletion(user_assignment)
        except Exception as e:
            self.logger.error(f"Ошибка при обработке удаления: {e}")

    def _find_extra_fields(
        self, data: Dict[str, Any], schema_fields: Set[str]
    ) -> Set[str]:
        """
        Находит поля в данных, которых нет в схеме.

        :param data: Данные из Kafka.
        :param schema_fields: Множество полей схемы.
        :return: Множество полей, которых нет в схеме.
        """
        alias_fields = {
            field.alias for field in UserEventSchemas.__fields__.values() if field.alias
        }
        all_schema_fields = schema_fields | alias_fields
        data_fields = set(data.keys())
        return data_fields - all_schema_fields
