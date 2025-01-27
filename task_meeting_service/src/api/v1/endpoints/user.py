from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.database.db import DatabaseSessionManager
from src.schemas.api.user import UserCreateSchema
from src.services.crud.user_service import UserService

router = APIRouter()


db_manager = DatabaseSessionManager()


@router.post("/users/")
async def create_user(user: UserCreateSchema):
    user_service = UserService(db_manager)
    user_id = await user_service.create_user(user.dict())
    return JSONResponse(content={"user_id": user_id})


@router.get("/users/{user_id}/")
async def get_user(user_id: int):
    user_service = UserService(db_manager)
    user = await user_service.get_user_by_id(user_id)
    return JSONResponse(content=user)
