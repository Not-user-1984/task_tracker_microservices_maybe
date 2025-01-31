from typing import List
from pydantic import BaseModel
from datetime import date, datetime


class TaskCreateSchema(BaseModel):
    description: str
    status: str
    deadline: date
    project_oid: str
    user_oid: str
    status_changed_at: date = date.today()


class TaskUpdateSchema(BaseModel):
    description: str
    status: str
    deadline: date
    user_name: str


class TaskResponse(BaseModel):
    id: int
    description: str
    status: str
    deadline: date
    project_oid: str
    user_oid: str
    status_changed_at: datetime

class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]