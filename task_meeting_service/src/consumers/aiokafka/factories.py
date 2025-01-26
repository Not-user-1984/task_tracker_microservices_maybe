from src.consumers.aiokafka.сonsumer import AIOKafkaMessageConsumer
from src.core.config import settings


def create_kafka_consumer() -> AIOKafkaMessageConsumer:
    return AIOKafkaMessageConsumer(
        topic=settings.kafka_topic,
        bootstrap_servers=settings.kafka_bootstrap_servers,
        group_id=settings.kafka_group_id,
    )
