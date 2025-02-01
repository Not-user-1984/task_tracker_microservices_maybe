from typing import Optional
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from src.database.db import db_manager
from src.schemas.api.task import (
    TaskCreateSchema,
    TaskListResponse,
    TaskUpdateSchema,
    TaskResponse,
)
from src.services.crud.task_service import TaskService
from src.auth.dependencies import get_current_user
from src.auth.security import TokenData

router = APIRouter()


@router.post("/tasks/")
async def create_task(task: TaskCreateSchema):
    task_service = TaskService(db_manager)
    task_id = await task_service.create_task(task)
    return JSONResponse(
        content={
            "task_id": task_id["id"],
        }
    )


@router.get("/tasks/{task_id}/")
async def get_task(
    task_id: int,
    current_user: TokenData = Depends(get_current_user)
    ):
    task_service = TaskService(db_manager)
    task = await task_service.get_task_by_id(task_id)
    task_dict = dict(task)
    return TaskResponse(**task_dict)


@router.put("/tasks/{task_id}/")
async def update_task(task_id: int, data: TaskCreateSchema):
    task_service = TaskService(db_manager)
    task = await task_service.update_task(task_id, data)
    task_dict = dict(task)
    return TaskResponse(**task_dict)


@router.get("/tasks/")
async def get_tasks(
    project_oid: Optional[str] = Query(None, description="Фильтр по project_oid"),
    user_oid: Optional[str] = Query(None, description="Фильтр по user_oid"),
):
    task_service = TaskService(db_manager)
    tasks = await task_service.get_tasks(project_oid, user_oid)

    tasks_response = [TaskResponse(**dict(task)) for task in tasks]

    return TaskListResponse(tasks=tasks_response, total=len(tasks_response))
