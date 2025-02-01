from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.database.db import db_manager
from src.schemas.api.user import (
    UserResponseSchema,
    UserUpdateSchema)
from src.services.crud.user_service import UserService


router = APIRouter()


@router.put("/users/{user_oid}/", response_model=UserResponseSchema)
async def update_user(user_oid: str, user_data: UserUpdateSchema):
    """
    Обновление данных пользователя по user_oid.

    :param user_oid: Уникальный идентификатор пользователя.
    :param user_data: Входные данные в формате UserUpdateSchema.
    :return: JSON с идентификатором обновленного пользователя.
    """
    user_service = UserService(db_manager)
    data = await user_service.update_user_by_oid(user_oid, user_data)
    return dict(data)


@router.get(
    "/users/{user_oid}/",
)
async def get_user(user_oid: str):
    user_service = UserService(db_manager)
    user = await user_service.get_user(user_oid)
    user_data = UserResponseSchema(**dict(user))
    return JSONResponse(content=user_data.dict())
