import asyncio
from typing import Any

from httpx import AsyncClient


async def get_data(client: AsyncClient) -> dict[str, Any]:
    response = await client.get('https://google.com')

    return response.text


async def main() -> None:
    client = AsyncClient()

    async with client:
        response = await get_data(client)
        print(response)

    async with client:
        response = await get_data(client)
        print(response)


if __name__ == '__main__':
    asyncio.run(main())
