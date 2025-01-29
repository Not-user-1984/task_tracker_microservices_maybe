from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.database.db import DatabaseSessionManager, db_manager
from src.schemas.api.user import UserCreateSchema, UserSchema
from src.services.crud.user_service import UserService


router = APIRouter()


@router.post("/users/", response_model=dict)
async def create_user(user: UserCreateSchema):
    """
    Создание пользователя с привязкой к проекту (опционально).
    :param user: Входные данные в формате UserCreateSchema
    :return: JSON с идентификатором созданного пользователя
    """
    user_service = UserService(db_manager)
    # Преобразование модели в словарь для передачи в сервис
    user_id = await user_service.create_user(user)
    return JSONResponse(content={"user_id": user_id})

@router.get("/users/{user_oid}/",)
async def get_user(user_oid: str):
    user_service = UserService(db_manager)
    user = await user_service.get_user(user_oid)
    user_data = UserSchema(**dict(user))
    return JSONResponse(content=user_data.dict())
