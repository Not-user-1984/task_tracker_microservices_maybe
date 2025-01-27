import asyncio
import json
import logging
from typing import List, Dict, Any, Optional
from src.consumers.consumer import MessageConsumer
from src.core.abstractions.message_handler import MessageHandler


class MessageConsumerService:
    """
    Сервис для потребления и обработки сообщений из любого источника.
    """

    def __init__(
        self,
        consumer: MessageConsumer,
        message_handler: MessageHandler,
        logger: logging.Logger,
    ):
        """
        Инициализация сервиса.

        :param consumer: Реализация потребителя сообщений.
        :param message_handler: Обработчик сообщений.
        :param logger: Логгер для записи событий.
        """
        self.consumer = consumer
        self.message_handler = message_handler
        self.logger = logger
        self.list_msg: List[Dict[str, Any]] = []
        self.stop_event = asyncio.Event()

    async def start(self) -> None:
        """
        Запускает потребитель сообщений и начинает обработку.
        """
        await self.consumer.start()
        self.logger.info("Message Consumer запущен.")
        try:
            async for msg in self.consumer.consume():
                await self.process_message(msg)
        except Exception as e:
            self.logger.error(f"Ошибка в Message Consumer: {e}")
        finally:
            await self.consumer.stop()
            self.logger.info("Message Consumer остановлен.")

    async def stop(self) -> None:
        """
        Останавливает потребитель сообщений.
        """
        self.stop_event.set()
        await self.consumer.stop()

    async def process_message(self, msg: Any) -> None:
        """
        Обрабатывает одно сообщение.

        :param msg: Сообщение от потребителя.
        """
        try:
            value = self._decode_message_value(msg.value)
            self.list_msg.append(value)
            if value:
                data = json.loads(value)
                payload = data.get("payload", {})
                if self._is_deleted(payload):
                    await self.message_handler.handle_deletion(
                        self._decode_key(msg.key)
                    )
                else:
                    await self.message_handler.handle_message(payload)
            else:
                await self.message_handler.handle_deletion(
                    self._decode_key(msg.key)
                )
        except json.JSONDecodeError as e:
            self.logger.error(f"Ошибка декодирования JSON: {e}")
            self.logger.error(f"Полученное сообщение: {msg.value}")
        except Exception as e:
            self.logger.error(f"Ошибка обработки сообщения: {e}")

    def _decode_message_value(self, value: Optional[bytes]) -> Optional[str]:
        """
        Декодирует значение сообщения из bytes в строку.

        :param value: Значение сообщения в формате bytes.
        :return: Декодированная строка или None, если значение отсутствует.
        """
        return value.decode("utf-8") if value else None

    def _is_deleted(self, payload: Dict[str, Any]) -> bool:
        """
        Проверяет, является ли сообщение сигналом об удалении.

        :param payload: Полезная нагрузка сообщения.
        :return: True, если объект удален, иначе False.
        """
        return payload.get("__deleted", "").lower() == "true"

    def _decode_key(self, key: Optional[bytes]) -> Optional[Dict[str, Any]]:
        """
        Декодирует ключ сообщения из bytes в словарь.

        :param key: Ключ сообщения в формате bytes.
        :return: Декодированный словарь или None, если ключ отсутствует.
        """
        if key:
            try:
                return json.loads(key.decode("utf-8"))
            except json.JSONDecodeError as e:
                self.logger.error(f"Ошибка декодирования ключа: {e}")
        return None

    def get_messages(self) -> List[Dict[str, Any]]:
        """
        Возвращает список всех обработанных сообщений.

        :return: Список сообщений.
        """
        return self.list_msg
