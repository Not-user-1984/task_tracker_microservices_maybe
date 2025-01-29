from typing import Optional
from pydantic import BaseModel
from datetime import date


class ProjectCreateSchema(BaseModel):
    project_name: str
    project_oid: str
    description: Optional[str] = "Автоматически созданный проект"
    release_date: Optional[date] = None
    status: Optional[str] = "active"


class ProjectUpdateSchema(BaseModel):
    name: str
    description: str
    release_date: date
    status: str
