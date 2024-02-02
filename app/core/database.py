from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine

from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker, MappedAsDataclass


from app.core.config import settings





DATABASE_URI = settings.POSTGRES_URI
DATABASE_PREFIX = settings.POSTGRES_SYNC_PREFIX
DATABASE_URL = f"{DATABASE_PREFIX}{DATABASE_URI}"

# async_engine = create_async_engine(
#     DATABASE_URL,
#     echo=False,
#     future=True
# )

# local_session = sessionmaker(
#     bind=async_engine,
#     class_=AsyncSession,
#     expire_on_commit=False
# )


# async def async_get_db() -> AsyncSession:
#     async_session = local_session

#     async with async_session() as db:
#         yield db
#         await db.commit()

engine = create_engine(
    DATABASE_URL
    # test_database_url
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
