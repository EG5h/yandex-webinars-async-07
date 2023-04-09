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
    session.add(MyTable(text_field='test1'))
    await session.commit()

    assert await fetch_important_data_from_database() == ['test', 'test1']


@respx.mock
@pytest.mark.asyncio()
async def test_fetch_from_internet() -> None:
    mocked_request = respx.get('https://httpbin.org/get').respond(json={'test': 'test'})
    result = await fetch_important_data_from_internet()
    assert mocked_request.call_count == 1
    assert result == {'test': 'test'}


@pytest.mark.asyncio()
@patch('my_async_app.some_functions.mock_me', return_value=666)
async def test_fetch_from_async_function(mocked_function: AsyncMock) -> None:
    result = await fetch_important_data_from_async_function()
    mocked_function.assert_awaited_once()
    assert result == 667


@pytest.mark.asyncio()
@patch.object(NiceClass, '_mock_me_too', return_value=666)
async def test_fetch_from_a_nice_class(mocked_function: AsyncMock) -> None:
    result = await NiceClass().get_nice_number()
    mocked_function.assert_awaited_once()
    assert result == 667


@pytest.mark.asyncio()
async def test_fastapi_app(client: AsyncClient) -> None:
    response = await client.get('/')
    assert response.status_code == 200
    assert response.json() == 42
