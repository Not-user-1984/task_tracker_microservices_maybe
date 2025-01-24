from fastapi import FastAPI, WebSocket
from aiokafka import AIOKafkaConsumer
import asyncio
import json
import logging

# Настройка логгера
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# Асинхронная функция для потребления сообщений из Kafka
async def consume_messages():
    consumer = AIOKafkaConsumer(
        'django_db.public.teams_userassignment',  # Правильное имя топика
        bootstrap_servers='kafka:9092',
        group_id='user-assignments-group',
        auto_offset_reset='earliest',
    )

    # Запуск Consumer
    await consumer.start()
    try:
        # Бесконечный цикл для чтения сообщений
        async for msg in consumer:
            logger.info(f"Получены данные: {msg}")
            # Декодируем JSON
            try:
                # data = json.loads(msg.value.decode('utf-8'))
                logger.info(f"Получены данные: {msg}")

                # Здесь можно отправить данные через WebSocket или сохранить в базу данных
                await broadcast_message(msg)
            except json.JSONDecodeError as e:
                logger.error(f"Ошибка декодирования JSON: {e}")
                logger.error(f"Полученное сообщение: {msg.value}")

    finally:
        # Остановка Consumer
        await consumer.stop()

# Запуск Consumer при старте FastAPI
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume_messages())

# WebSocket для отправки сообщений в реальном времени
connected_clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            # Ожидание сообщений от клиента (необязательно)
            data = await websocket.receive_text()
            logger.info(f"Сообщение от клиента: {data}")
    except Exception as e:
        logger.error(f"Ошибка WebSocket: {e}")
    finally:
        connected_clients.remove(websocket)

# Функция для отправки сообщений всем подключенным клиентам
async def broadcast_message(data):
    for client in connected_clients:
        try:
            await client.send_json(data)
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения клиенту: {e}")

# Базовый эндпоинт для проверки работоспособности
@app.get("/")
def read_root():
    return {"message": "Микросервис для обработки назначений пользователей"}