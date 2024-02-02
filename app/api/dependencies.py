from typing import Annotated

from app.core.security import SECRET_KEY, ALGORITHM, oauth2_scheme
from app.core.config import settings

from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from fastapi import (
    Depends,
    HTTPException,
    Request
)
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.core.models import TokenData
from app.models.user import User
from app.crud.crud_users import crud_users
from app.api.exceptions import credentials_exception, privileges_exception

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)]
) -> User:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        email:str = payload.get("sub")
        if email is None:
            raise credentials_exception
        
        token_data = TokenData(email=email)
    
    except JWTError:
        raise credentials_exception

    user = crud_users.get(db=db, email=token_data.email)

    if user and not user["is_deleted"]:
        return user


async def get_current_superuser(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if not current_user["is_superuser"]:
        raise privileges_exception

    return current_user


