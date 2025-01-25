from pydantic import BaseModel, Field
from typing import Optional


class UserEventSchemas(BaseModel):
    id: int
    project_id: int
    team_id: Optional[int] = None
    user_id: int
    project_name: Optional[str] = None
    team_name: Optional[str] = None
    user_role: Optional[str] = None
    user_oid: Optional[str] = None
    user_email: Optional[str] = None
    user_name: Optional[str] = None
    deleted: Optional[str] = Field(None, alias="__deleted")
    op: Optional[str] = Field(None, alias="__op")
    ts_ms: Optional[int] = Field(None, alias="__ts_ms")

    class Config:
        allow_population_by_field_name = True
