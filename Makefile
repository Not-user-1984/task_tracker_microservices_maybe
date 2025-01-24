# Переменные
DOCKER_COMPOSE_FILE=docker-compose.yml

# Основной сервис Django (user_team_service)
SERVICE_NAME=user_team_service
DB_SERVICE_NAME = db_django  # Имя сервиса базы данных в docker-compose.yml
DB_USER = django_user          # Пользователь базы данных
DB_NAME = django_db       # Имя базы данных

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
makemigrate:
	docker-compose -f $(DOCKER_COMPOSE_FILE) exec $(SERVICE_NAME) python manage.py makemigrations

# Создание суперпользователя Django
dj_cr_s_user:
	docker-compose -f $(DOCKER_COMPOSE_FILE) exec $(SERVICE_NAME) python manage.py createsuperuser

# Запуск shell внутри контейнера Django
sh-django:
	docker-compose -f $(DOCKER_COMPOSE_FILE) exec $(SERVICE_NAME) sh
Для создания команды в Makefile, которая позволяет войти в базу данных PostgreSQL, запущенную в Docker-контейнере, можно добавить следующее:

# Команда для входа в базу данных
db:
	docker-compose -f $(DOCKER_COMPOSE_FILE) exec $(DB_SERVICE_NAME) psql -U $(DB_USER) -d $(DB_NAME)
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