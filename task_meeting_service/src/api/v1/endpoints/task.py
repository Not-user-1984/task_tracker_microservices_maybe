from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.database.db import db_manager
from src.schemas.api.task import TaskCreateSchema, TaskUpdateSchema
from src.services.crud.task_service import TaskService

router = APIRouter()


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
async def update_task(task_id: int, data: TaskCreateSchema):
    task_service = TaskService(db_manager)
    task = await task_service.update_task(task_id, data)
    data = TaskCreateSchema(**dict(task))
    return JSONResponse(content=data)
    # return JSONResponse(content={f"message:  {task}"})
