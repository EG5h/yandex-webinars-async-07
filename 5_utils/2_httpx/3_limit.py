import asyncio
from typing import Any

from httpx import AsyncClient, Limits


async def get_data(client: AsyncClient, i: int) -> dict[str, Any]:
    print('Getting data for ', i)
    response = await client.get('request')
    print('Got data for ', i)
    response.raise_for_status()
    return response.json()


async def main() -> None:
    client = AsyncClient(
        base_url='http://mockbin.com/',
        limits=Limits(max_connections=2),
        timeout=60,
    )
    async with client:
        responses = await asyncio.gather(*(get_data(client, i) for i in range(20)))

    print(responses)


if __name__ == '__main__':
    asyncio.run(main())
