from pydantic import BaseModel
from datetime import date

class TaskCreateSchema(BaseModel):
    description: str
    status: str
    deadline: date
    project_id: int
    user_name: str

class TaskUpdateSchema(BaseModel):
    description: str
    status: str
    deadline: date
    user_name: str
