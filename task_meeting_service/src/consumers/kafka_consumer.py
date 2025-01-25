import asyncio
import json
import logging
from typing import List, Dict, Any, Optional, Set
from aiokafka import AIOKafkaConsumer, ConsumerRecord
from src.schemas.user_events import UserEventSchemas
from src.services.user_assignment_service import UserEventService


class KafkaConsumerService:
    """
    Сервис для потребления сообщений из Kafka и их обработки.
    """

    def __init__(
        self,
        topic: str,
        bootstrap_servers: str,
        group_id: str,
        logger: logging.Logger,
    ):
        """
        Инициализация Kafka Consumer.

        :param topic: Название топика Kafka.
        :param bootstrap_servers: Адреса серверов Kafka.
        :param group_id: Идентификатор группы потребителей.
        :param logger: Логгер для записи событий.
        """
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.logger = logger
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset="earliest",
        )
        self.list_msg: List[Dict[str, Any]] = []
        self.user_assignment_service = UserEventService(logger)
        self.stop_event = asyncio.Event()

    async def start(self) -> None:
        """
        Запуск Kafka Consumer и начало обработки сообщений.
        """
        await self.consumer.start()
        self.logger.info(f"Kafka Consumer запущен для топика: {self.topic}")
        try:
            async for msg in self.consumer:
                # self.logger.debug(f"Получено сообщение: {msg}")
                await self.process_message(msg)
        except Exception as e:
            self.logger.error(f"Ошибка в Kafka Consumer: {e}")
        finally:
            await self.consumer.stop()
            self.logger.info("Kafka Consumer остановлен.")

    async def stop(self) -> None:
        self.stop_event.set()

    async def process_message(self, msg: ConsumerRecord) -> None:
        """
        Обработка одного сообщения из Kafka.

        :param msg: Сообщение из Kafka.
        """
        try:
            value = self._decode_message_value(msg.value)
            self.list_msg.append(value)
            if value:
                data = json.loads(value)
                payload = data.get("payload", {})
                if self._is_deleted(payload):
                    await self._handle_deletion(msg.key)
                else:
                    await self._handle_user_assignment(payload)
            else:
                await self._handle_deletion(msg.key)
        except json.JSONDecodeError as e:
            self.logger.error(f"Ошибка декодирования JSON: {e}")
            self.logger.error(f"Полученное сообщение: {msg.value}")
        except Exception as e:
            self.logger.error(f"Ошибка обработки сообщения: {e}")

    def _decode_message_value(self, value: Optional[bytes]) -> Optional[str]:
        """
        Декодирование значения сообщения из bytes в строку.

        :param value: Значение сообщения в формате bytes.
        :return: Декодированная строка или None, если значение отсутствует.
        """
        return value.decode("utf-8") if value else None

    def _is_deleted(self, payload: Dict[str, Any]) -> bool:
        """
        Проверка, является ли сообщение сигналом об удалении.

        :param payload: Полезная нагрузка сообщения.
        :return: True, если объект удален, иначе False.
        """
        return payload.get("__deleted", "").lower() == "true"

    async def _handle_deletion(self, key: Optional[bytes]) -> None:
        """
        Обработка удаления объекта.

        :param key: Ключ сообщения.
        """
        decoded_key = self._decode_key(key)
        await self.user_assignment_service.handle_deletion(decoded_key)

    def _decode_key(self, key: Optional[bytes]) -> Optional[Dict[str, Any]]:
        """
        Декодирование ключа сообщения из bytes в словарь.

        :param key: Ключ сообщения в формате bytes.
        :return: Декодированный словарь или None, если ключ отсутствует.
        """
        if key:
            try:
                return json.loads(key.decode("utf-8"))
            except json.JSONDecodeError as e:
                self.logger.error(f"Ошибка декодирования ключа: {e}")
        return None

    async def _handle_user_assignment(self, payload: Dict[str, Any]) -> None:
        """
        Обработка создания или обновления объекта UserAssignment.

        :param payload: Полезная нагрузка сообщения.
        """
        try:
            schema_fields = set(UserEventSchemas.__fields__.keys())

            extra_fields = self._find_extra_fields(payload, schema_fields)

            if extra_fields:
                self.logger.warning(
                    f"Обнаружены поля, которых нет в схеме: {extra_fields}. "
                    f"Добавьте их в модель UserAssignmentSchema."
                )

            user_assignment = UserEventSchemas(**payload)
            self.logger.info(f"Обработан объект: {user_assignment}")

            operation = payload.get("__op")
            if operation == "c":
                await self.user_assignment_service.handle_creation(user_assignment)
            elif operation == "u":
                await self.user_assignment_service.handle_update(user_assignment)
        except Exception as e:
            self.logger.error(f"Ошибка обработки сообщения: {e}")

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

    def get_messages(self) -> List[Dict[str, Any]]:
        """
        Получение списка всех обработанных сообщений.

        :return: Список сообщений.
        """
        return self.list_msg
