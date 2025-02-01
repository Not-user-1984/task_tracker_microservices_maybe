from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.auth.security import verify_token
from jose import JWTError, jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_data = verify_token(token)
    except JWTError:
        raise credentials_exception
    return token_data
