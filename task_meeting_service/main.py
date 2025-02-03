import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
from src.consumers.consumer_мessage import MessageConsumerService
from src.handlers.events.user_event_handler import UserEventHandler
from src.consumers.aiokafka.factories import create_kafka_consumer

from src.api.v1.endpoints.projects import router as projects_router
from src.api.v1.endpoints.user import router as user_router
from src.api.v1.endpoints.task import router as task_router
from src.api.v1.endpoints.auth import router as auth_router
from src.database.db import db_manager
from src.database.database_initializer import create_tables

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(user_router, prefix="/api", )
app.include_router(task_router, prefix="/api")
app.include_router(projects_router, prefix="/api")
app.include_router(projects_router, prefix="/api")
app.include_router(auth_router, prefix="/api")

consumer = create_kafka_consumer()
handler = UserEventHandler(logger, db_manager)
kafka_consumer_service = MessageConsumerService(consumer, handler, logger)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def init_db(db_manager):
    await create_tables(db_manager)


@app.on_event("startup")
async def startup_event():
    logger.info("Запуск Kafka Consumer...")
    asyncio.create_task(kafka_consumer_service.start())
    await db_manager.connect()
    await init_db(db_manager)
    logger.info("База данных инициализирована")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Остановка Kafka Consumer...")
    try:
        await kafka_consumer_service.stop()
    except asyncio.TimeoutError:
        logger.error(
            "Не удалось остановить Kafka Consumer в течение 10 секунд"
            )
