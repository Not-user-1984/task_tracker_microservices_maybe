from typing import Any, Dict
from src.services.crud.user_service import UserService
from src.services.crud.project_service import ProjectService
from src.services.crud.task_service import TaskService
from src.schemas.user_events import UserEventSchemas
# from src.core.abstractions.message_handler import MessageHandler


class UserEventService():
    def __init__(self, logger, db):
        self.logger = logger
        self.user_service = UserService(db)
        self.project_service = ProjectService(db)
        self.task_service = TaskService(db)

    async def handle_creation(self, user_assignment: UserEventSchemas):
        # Проверяем пользователя
        user = await self.user_service.get_user(user_assignment.user_oid)
        if not user:
            await self.user_service.create_user(user_assignment)
            self.logger.info(f"Создан пользователь: {user_assignment.user_name}")
        
        project = await self.project_service.get_project(user_assignment.project_name)
        if not project:
            project_data = {
                "project_name": user_assignment.project_name,
                "status": "active",
                "description": "Автоматически созданный проект",
                "release_date": None,
            }
            await self.project_service.create_project(project_data)
            self.logger.info(f"Создан проект: {user_assignment.project_name}")
            project = await self.project_service.get_project(user_assignment.project_name)

        # Проверяем задачу
        if user_assignment.project_name and user_assignment.user_name:
            task_description = f"Task for {user_assignment.user_name} in {user_assignment.project_name}"
            task = await self.task_service.get_task(task_description, project["id"])
            if not task:
                task_data = {
                    "description": task_description,
                    "status": "in_progress",
                    "project_id": project["id"],
                    "user_name": user_assignment.user_name,
                    "status_changed_at": None,
                    "deadline": None,
                }
                await self.task_service.create_task(task_data)
                self.logger.info(f"Создана задача: {task_description}")


    async def handle_deletion(self, key: Dict[str, Any]):
        # Удаляем задачу, если указаны описание и проект
        if "description" in key and "project_id" in key:
            await self.task_service.delete_task(key["description"], key["project_id"])
            self.logger.info(f"Удалена задача: {key['description']} из проекта {key['project_id']}")
        
        # Удаляем проект
        if "project_name" in key:
            await self.project_service.delete_project(key["project_name"])
            self.logger.info(f"Удален проект: {key['project_name']}")
        
        # Удаляем пользователя
        if "user_oid" in key:
            await self.user_service.delete_user(key["user_oid"])
            self.logger.info(f"Удален пользователь: {key['user_oid']}")

    async def handle_update(self, user_assignment: UserEventSchemas):
        # Обновление пользователя
        if user_assignment.user_oid:
            updates = {
                "user_name": user_assignment.user_name,
                "user_email": user_assignment.user_email,
                "user_role": user_assignment.user_role,
            }
            updates = {k: v for k, v in updates.items() if v is not None}
            await self.user_service.update_user(user_assignment.user_oid, updates)
            self.logger.info(f"Обновлен пользователь: {user_assignment.user_oid}")
        
        # Обновление проекта
        if user_assignment.project_name:
            updates = {
                "status": "active",
                "description": "Обновленное описание",
            }
            await self.project_service.update_project(user_assignment.project_name, updates)
            self.logger.info(f"Обновлен проект: {user_assignment.project_name}")

        # Обновление задачи
        if user_assignment.project_name and user_assignment.user_name:
            task_description = f"Task for {user_assignment.user_name} in {user_assignment.project_name}"
            updates = {
                "status": "completed",
                "status_changed_at": user_assignment.ts_ms,
            }
            await self.task_service.update_task(task_description, user_assignment.project_id, updates)
            self.logger.info(f"Обновлена задача: {task_description}")
