import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import asyncio
from src.consumers.kafka_consumer import KafkaConsumerService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()
kafka_consumer_service = KafkaConsumerService(
    topic="django_db.public.teams_userassignment",
    bootstrap_servers="kafka:9092",
    group_id="user-assignments-group",
    logger=logger,
)


@app.on_event("startup")
async def startup_event():
    logger.info("Запуск Kafka Consumer...")
    asyncio.create_task(kafka_consumer_service.start())


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Остановка Kafka Consumer...")
    try:
        await asyncio.wait_for(kafka_consumer_service.stop(), timeout=10.0)
    except asyncio.TimeoutError:
        logger.error("Не удалось остановить Kafka Consumer в течение 10 секунд")

# Базовый эндпоинт для проверки работоспособности
@app.get("/task/")
def read_root():
    return JSONResponse(content=kafka_consumer_service.get_messages())
