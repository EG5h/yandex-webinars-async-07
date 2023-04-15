import asyncio
import time

import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from db import Session

app = FastAPI()


@app.get('/')
def root() -> int:
    """
    Синхронный ендпоинт, максимум 40 параллельных запросов
    """
    time.sleep(1)
    return 1


@app.get('/')
async def root() -> int:
    """
    Асинхронный ендпоинт, число параллельных запросов не ограничено (только железом)
    """
    await asyncio.sleep(1)
    return 1


async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session


@app.get('/')
async def root(session: AsyncSession = Depends(get_session)) -> int:
    """
    Асинхронный ендпоинт, ограничено соединениями с БД. Сессия открывается
    в начале запроса и закрывается в конце. Мы просто так держим сессию открытой когда происходит sleep
    """
    await session.execute(text('SELECT pg_sleep(1)'))
    await asyncio.sleep(1)
    return 1


@app.get('/')
async def root() -> int:
    """
    Асинхронный ендпоинт, ограничено соединениями с БД. Но при этом сессия создается
    только когда нам это нужно, эффективно расходуя connection pool
    """
    async with Session() as session:
        await session.execute(text('SELECT pg_sleep(1)'))

    await asyncio.sleep(1)
    return 1


if __name__ == '__main__':
    uvicorn.run('main:app', workers=1)
