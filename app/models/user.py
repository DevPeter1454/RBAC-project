from typing import Optional, List
import uuid as uuid_pkg
from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, MappedAsDataclass, DeclarativeBase

from app.core.database import Base


class Base(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses"""


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False
    )
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default_factory=datetime.utcnow
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    is_deleted: Mapped[bool] = mapped_column(default=False, index=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    

    
