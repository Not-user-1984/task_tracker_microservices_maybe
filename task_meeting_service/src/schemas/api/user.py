from pydantic import BaseModel, EmailStr


class UserCreateSchema(BaseModel):
    user_oid: str
    user_name: str
    user_email: EmailStr
    user_role: str | None = None
    project_oid: str | None = None


class UserResponseSchema(BaseModel):
    id: int
    user_oid: str
    user_name: str
    user_email: str
    user_role: str | None
    project_oid: str | None


class UserUpdateSchema(BaseModel):
    project_oid: str
