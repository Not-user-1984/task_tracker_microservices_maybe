from pydantic import BaseModel
from datetime import date

class ProjectCreateSchema(BaseModel):
    name: str
    description: str
    release_date: date
    status: str

class ProjectUpdateSchema(BaseModel):
    name: str
    description: str
    release_date: date
    status: str
