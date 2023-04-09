from typing import Callable, Union

from sqlalchemy.ext.asyncio import (
    AsyncConnection, AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from my_async_app.config import settings


def create_engine() -> AsyncEngine:
    return create_async_engine(settings.database_url)


def create_sessionmaker(bind_engine: Union[AsyncEngine, AsyncConnection]) -> Callable[..., AsyncSession]:
    return async_sessionmaker(
        bind=bind_engine,
        autoflush=False,
        expire_on_commit=False,
        future=True,
        class_=AsyncSession,
    )


engine = create_engine()
Session = create_sessionmaker(engine)


class Base(DeclarativeBase):
    pass
