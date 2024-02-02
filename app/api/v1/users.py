from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
import fastapi
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.crud_users import crud_users
from app.core.security import get_password_hash

from app.schemas.users import UserCreate, UserCreateInternal, UserRead


router = fastapi.APIRouter(tags=["users"])


@router.post("/user", status_code=201)
async def write_user(
    request: Request,
    user: UserCreate,
    db: Annotated[Session, Depends(get_db)]
):
    email_row = await crud_users.exists(db, email=user.email)
    if email_row:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_internal_dict = user.model_dump()
    user_internal_dict["hashed_password"] = get_password_hash(
        password=user_internal_dict["password"])
    del user_internal_dict["password"]

    user_internal = UserCreateInternal(**user_internal_dict)
    user = await crud_users.create(db=db, object=user_internal)

    # await send_email.send_email(subject="Welcome to FastAPI app", email_to=user.email)

    return {"message": "User created successfully"}


@router.get("/user")
async def read_user(
    request: Request,
    db: Annotated[Session, Depends(get_db)]
):
    return {"test": "done"}
