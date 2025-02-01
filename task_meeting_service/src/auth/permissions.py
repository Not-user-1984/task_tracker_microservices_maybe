from fastapi import Depends, HTTPException, status
from src.auth.security import TokenData
from src.auth.dependencies import get_current_user


def role_required(required_role: str):
    def decorator(current_user: TokenData = Depends(get_current_user)):
        if current_user.user_role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )
        return current_user

    return decorator
