from typing import AsyncIterator
from aiokafka import AIOKafkaConsumer, ConsumerRecord
from src.consumers.consumer import MessageConsumer


class AIOKafkaMessageConsumer(MessageConsumer):
    def __init__(self, topic: str, bootstrap_servers: str, group_id: str):
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            auto_offset_reset="earliest",
        )

    async def start(self) -> None:
        await self.consumer.start()

    async def stop(self) -> None:
        await self.consumer.stop()

    async def consume(self) -> AsyncIterator[ConsumerRecord]:
        async for msg in self.consumer:
            yield msg
