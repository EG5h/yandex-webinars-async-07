import asyncio
import time

import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from db import Session

app = FastAPI()


async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session


@app.get('/')
async def root() -> int:
    async with Session() as session:
        await session.execute(text('SELECT pg_sleep(1)'))

    await asyncio.sleep(1)
    return 1


if __name__ == '__main__':
    uvicorn.run('main:app', workers=1)
