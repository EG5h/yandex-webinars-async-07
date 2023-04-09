from unittest.mock import AsyncMock, patch

import pytest
import respx
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from my_async_app.db_models import MyTable
from my_async_app.some_functions import (
    NiceClass, fetch_important_data_from_async_function, fetch_important_data_from_database,
    fetch_important_data_from_internet,
)


@pytest.mark.asyncio()
async def test_fetch_from_db(session: AsyncSession) -> None:
    session.add(MyTable(text_field='test'))
    session.add(MyTable(text_field='test2'))
    await session.commit()

    result = await fetch_important_data_from_database()

    assert result == ['test', 'test2']


@respx.mock
@pytest.mark.asyncio()
async def test_fetch_from_internet() -> None:
    respond = {'test': 'test'}
    respx.get('https://httpbin.org/get').respond(json=respond)
    result = await fetch_important_data_from_internet()

    assert result == respond


@pytest.mark.asyncio()
@patch('my_async_app.some_functions.mock_me')
async def test_fetch_from_async_function(mocked_function: AsyncMock) -> None:
    mocked_function.return_value = 2007

    assert await fetch_important_data_from_async_function() == 2007
    mocked_function.assert_awaited()


@pytest.mark.asyncio()
@patch.object(NiceClass, '_mock_me_too', return_value=2007)
async def test_fetch_from_a_nice_class(mocked_function: AsyncMock) -> None:
    nice_object = NiceClass()

    assert await nice_object.get_nice_number() == 2007


@pytest.mark.asyncio()
async def test_fastapi_app(client: AsyncClient) -> None:
    response = await client.get('/')

    assert response.status_code == 200
    assert response.text == '42'
