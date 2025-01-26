import logging
from abc import ABC, abstractmethod
from typing import Dict, Any

from pydantic import BaseModel


class MessageHandler(ABC):
    """
    Абстрактный класс для обработки событий пользователя.
    """

    def __init__(self, logger: logging.Logger):
        """
        Инициализация сервиса.

        :param logger: Логгер для записи событий.
        """
        self.logger = logger

    @abstractmethod
    async def handle_deletion(self, key: Dict[str, Any]) -> None:
        """
        Обработка удаления объекта.

        :param key: Ключ удаляемого объекта.
        """
        pass

    @abstractmethod
    async def handle_creation(self, user_assignment: BaseModel) -> None:
        """
        Обработка создания объекта.

        :param user_assignment: Данные создаваемого объекта.
        """
        pass

    @abstractmethod
    async def handle_update(self, user_assignment: BaseModel) -> None:
        """
        Обработка обновления объекта.

        :param user_assignment: Данные обновляемого объекта.
        """
        pass