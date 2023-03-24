import time
from asyncio import sleep
from typing import Any


async def my_function(
    ctx: dict[str, Any], delay: int,
):
    await sleep(delay)
