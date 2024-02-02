from typing import Optional, List
import uuid as uuid_pkg
from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, MappedAsDataclass, DeclarativeBase

from app.core.database import Base

class Base(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses"""


class Token(Base):
    __tablename__ = "token"
    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False
    )
    token: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, )
