from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.auth.security import (
    create_access_token,
    verify_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from src.services.crud.user_service import UserService
from src.database.db import db_manager

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_service = UserService(db_manager)
    user = await user_service.get_user(
        form_data.username
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    data = dict(user)
    print(data)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": data['user_oid'], "role": data['user_role']},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
