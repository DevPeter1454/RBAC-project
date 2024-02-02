from typing import Annotated, Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.core.models import UUIDModel, TimestampModel, PersistentDeletion


class UserBase(BaseModel):
    name: Annotated[
        str,
        Field(min_length=2, max_length=30, examples=["User Userson"])
    ]
    email: Annotated[
        EmailStr,
        Field(examples=["user.userson@example.com"])
    ]
    is_superuser: Annotated[
        bool,
        Field(default=False)
    ]

    

class UserCreate(UserBase):
    model_config = ConfigDict(extra='forbid')

    password: Annotated[
        str,
        Field(
            pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$", examples=["Str1ngst!"])
    ]


class UserCreateInternal(UserBase):
    hashed_password: str


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: Annotated[
        Optional[str],
        Field(
            min_length=2,
            max_length=30,
            examples=["User Userberg"],
            default=None
        )
    ]
    email: Annotated[
        Optional[EmailStr],
        Field(
            examples=["user.userberg@example.com"],
            default=None
        )
    ]
    


class UserUpdateInternal(UserUpdate):
    updated_at: datetime


class UserTierUpdate(BaseModel):
    tier_id: int


class UserDelete(BaseModel):
    model_config = ConfigDict(extra='forbid')

    is_deleted: bool
    deleted_at: datetime


class UserRestoreDeleted(BaseModel):
    is_deleted: bool


class UserRead(BaseModel):
    id:int
    name: Annotated[
        Optional[str],
        Field(
            min_length=2,
            max_length=30,
            examples=["User Userberg"],
            default=None
        )
    ]
    email: Annotated[
        EmailStr,
        Field(examples=["user.userson@example.com"])
    ]
    is_superuser: Annotated[
        bool,
        Field(default=False)
    ]

    class Config:
        from_attributes = True

