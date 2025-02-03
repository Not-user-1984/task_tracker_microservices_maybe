# Управление командами IT


## Описание проекта
Этот проект больше построен для практики работы с Kafka и микросервисной архитектуры, так что некоторые моменты в самих микросервисах опущены.


## Видео-демонстрация работы проекта.
```

```


## Стек технологий
- **Языки программирования:** Python (Django, FastAPI), Go
- **Базы данных:** PostgreSQL
- **Месседж-брокер:** Kafka
- **Change Data Capture (CDC):** Debezium Connector
- **Контейнеризация и оркестрация:** Docker, Docker Compose
- **Инструменты DevOps:** Makefile
- **Система логирования и мониторинга:** Kafka UI

## Состав проекта
Проект состоит из трех микросервисов:

### 1. `user_team_service` (Django)
- Отвечает за верхнеуровневое управление командами.
- Построен на стандартной админке Django.
- Основная функциональность — назначение команд.
- Позволяет прокидывать URL на заявки на оформление.

### 2. `task_meeting_service` (FastAPI)
- Управляет созданием задач и назначением дедлайнов и статусов.
- Возможно расширение под управление профилями пользователей.
- В перспективе можно выделить отдельный микросервис.

### 3. `notification_email` (Go)
- Простой микросервис для отправки email-уведомлений.

## Дизайн системы

Главный микросервис — `user_team_service`, он не знает о существовании других сервисов. Вся коммуникация проходит через базу данных с использованием **Debezium Connector**.

1. **Debezium Connector** следит за изменениями в таблице `teams_userassignment` в `db_django`.
2. При изменениях данные отправляются в **Kafka-топик**.
3. `task_meeting_service` обрабатывает сообщения и создаёт нужные записи в своей БД.
4. `notification_email` отправляет email-уведомления пользователям.




## Тестирование

В проекте написаны тесты только для task_meeting_service. Запустить их можно с помощью команды:
```
make tests-fastapi
```
Для user_team_service тесты не написаны, так как используются стандартные операции Django-админки.


## Развертывание проекта

1. Заполните все `example.env` в `task_meeting_service` и `user_team_service`.
2. Запустите проект:
   ```sh
   docker-compose up -d
   ```
3. Если контейнер `debezium-connector` падает, попробуйте перезапустить `zookeeper`:
   ```sh
   docker-compose restart zookeeper
   ```
4. После развертывания настройте Debezium Connector через UI: `http://localhost:8010`.
   - При создании нового коннектора выберите `PostgresConnector` и настройте его:
   
```json
{
  "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
  "database.user": "django_user",
  "database.dbname": "django_db",
  "transforms.extractKey.field": "id",
  "slot.name": "debezium_slot",
  "publication.name": "debezium_pub",
  "transforms": "unwrap,extractKey",
  "database.server.name": "db_django",
  "transforms.extractKey.type": "org.apache.kafka.connect.transforms.ExtractField$Key",
  "database.port": "5432",
  "plugin.name": "pgoutput",
  "topic.prefix": "django_db",
  "database.hostname": "db_django",
  "database.password": "django_password",
  "transforms.unwrap.drop.tombstones": "false",
  "transforms.unwrap.add.fields": "op,ts_ms",
  "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
  "table.include.list": "public.teams_userassignment"
}
```

## Команды управления

### Основные команды Makefile:

```sh
# Запуск всех сервисов
make up

# Запуск только Django (user_team_service)
make up-django

# Остановка всех сервисов
make down

# Перезапуск Django
make restart-django

# Просмотр логов Django
make logs-django

# Остановка и удаление всех контейнеров, volumes и networks
make clean

# Запуск миграций Django
make migrate

# Создание суперпользователя Django
make createsuperuser

# Вход в shell Django
make sh-django

# Вход в базу данных PostgreSQL
make db

# Проверка состояния контейнеров
make ps

# Очистка неиспользуемых данных Docker
make prune

# Настройка Debezium Connector
make setup-connector

# Логи FastAPI сервиса
make logs-fastapi

# Вход в контейнер FastAPI
make sh-fastapi

# Запуск тестов FastAPI
make tests-fastapi
```

### Дополнительные команды:

```sh
make help
```
Выведет список доступных команд.

---