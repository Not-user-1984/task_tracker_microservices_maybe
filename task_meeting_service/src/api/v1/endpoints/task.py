from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.database.db import DatabaseSessionManager
from src.schemas.api.task import TaskCreateSchema, TaskUpdateSchema
from src.services.crud.task_service import TaskService

router = APIRouter()

db_manager = DatabaseSessionManager()


@router.post("/tasks/")
async def create_task(task: TaskCreateSchema):
    task_service = TaskService(db_manager)
    task_id = await task_service.create_task(task.dict())
    return JSONResponse(content={"task_id": task_id})


@router.get("/tasks/{task_id}/")
async def get_task(task_id: int):
    task_service = TaskService(db_manager)
    task = await task_service.get_task_by_id(task_id)
    return JSONResponse(content=task)


@router.put("/tasks/{task_id}/")
async def update_task(task_id: int, task: TaskUpdateSchema):
    task_service = TaskService(db_manager)
    await task_service.update_task(task_id, task.dict())
    return JSONResponse(content={"message": "Task updated successfully"})
