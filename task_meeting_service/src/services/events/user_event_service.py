import logging
from typing import Dict, Any

from src.schemas.user_events import UserEventSchemas
from src.core.abstractions.message_handler import MessageHandler


class UserEventService(MessageHandler):
    def __init__(self, logger):
        self.logger = logger

    async def handle_deletion(self, key: Dict[str, Any]):
        self.logger.info(f"Объект удален. Ключ: {key}")

    async def handle_creation(self, user_assignment: UserEventSchemas):
        self.logger.info(f"Создание объекта: {user_assignment}")

    async def handle_update(self, user_assignment: UserEventSchemas):
        self.logger.info(f"Обновление объекта: {user_assignment}")
