import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import asyncio
from src.services.events.consumer_service import MessageConsumerService
from src.handlers.events.user_event_handler import UserEventHandler
from src.consumers.aiokafka.factories import create_kafka_consumer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()


consumer = create_kafka_consumer()
handler = UserEventHandler(logger)
kafka_consumer_service = MessageConsumerService(consumer, handler, logger)


@app.on_event("startup")
async def startup_event():
    logger.info("Запуск Kafka Consumer...")
    asyncio.create_task(kafka_consumer_service.start())


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Остановка Kafka Consumer...")
    try:
        await kafka_consumer_service.stop()
    except asyncio.TimeoutError:
        logger.error("Не удалось остановить Kafka Consumer в течение 10 секунд")


@app.get("/task/")
def read_root():
    return JSONResponse(content=kafka_consumer_service.get_messages())
