# Переменные
DOCKER_COMPOSE_FILE=docker-compose.yml

# Основной сервис Django (user_team_service)
SERVICE_NAME=user_team_service

# Дополнительные сервисы (например, task_meeting_service, redis, db и т.д.)
# SERVICE_NAME_TASK_MEETING=task_meeting_service
# SERVICE_NAME_REDIS=redis
# SERVICE_NAME_DB=postgres_db

# Сборка и запуск всех сервисов
up:
	docker-compose -f $(DOCKER_COMPOSE_FILE) up --build -d

# Сборка и запуск только Django (user_team_service)
up-django:
	docker-compose -f $(DOCKER_COMPOSE_FILE) up --build -d $(SERVICE_NAME)

# Остановка всех сервисов
down:
	docker-compose -f $(DOCKER_COMPOSE_FILE) down

# Перезапуск Django (user_team_service)
restart-django:
	docker-compose -f $(DOCKER_COMPOSE_FILE) restart $(SERVICE_NAME)

# Просмотр логов Django (user_team_service)
logs-django:
	docker-compose -f $(DOCKER_COMPOSE_FILE) logs -f $(SERVICE_NAME)

# Остановка и удаление всех контейнеров, volumes и networks
clean:
	docker-compose -f $(DOCKER_COMPOSE_FILE) down -v

# Запуск миграций Django
migrate:
	docker-compose -f $(DOCKER_COMPOSE_FILE) exec $(SERVICE_NAME) python manage.py migrate

# Создание суперпользователя Django
createsuperuser:
	docker-compose -f $(DOCKER_COMPOSE_FILE) exec $(SERVICE_NAME) python manage.py createsuperuser

# Запуск shell внутри контейнера Django
exec-django:
	docker-compose -f $(DOCKER_COMPOSE_FILE) exec $(SERVICE_NAME) sh

# Проверка состояния всех контейнеров
ps:
	docker-compose -f $(DOCKER_COMPOSE_FILE) ps

# Очистка всех неиспользуемых данных Docker (осторожно!)
prune:
	docker system prune -f

# Помощь (список доступных команд)
help:
	@echo "Доступные команды:"
	@echo "  make up               - Сборка и запуск всех сервисов"
	@echo "  make up-django        - Сборка и запуск только Django (user_team_service)"
	@echo "  make down             - Остановка всех сервисов"
	@echo "  make restart-django   - Перезапуск Django (user_team_service)"
	@echo "  make logs-django      - Просмотр логов Django (user_team_service)"
	@echo "  make clean            - Остановка и удаление всех контейнеров, volumes и networks"
	@echo "  make migrate          - Запуск миграций Django"
	@echo "  make createsuperuser  - Создание суперпользователя Django"
	@echo "  make exec-django      - Запуск shell внутри контейнера Django"
	@echo "  make ps               - Проверка состояния всех контейнеров"
	@echo "  make prune            - Очистка всех неиспользуемых данных Docker"
	@echo "  make help             - Показать это сообщение"