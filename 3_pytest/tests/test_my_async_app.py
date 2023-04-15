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
    """
    Тесты на асинхронные функции должны быть помечены как @pytest.mark.asyncio()
    Для каждого теста создаем отдельно объекты БД
    """
    session.add(MyTable(text_field='test'))
    session.add(MyTable(text_field='test1'))
    await session.commit()

    assert await fetch_important_data_from_database() == ['test', 'test1']


@respx.mock
@pytest.mark.asyncio()
async def test_fetch_from_internet() -> None:
    """
    Используем respx для моков http запросов
    respx работает только с httpx
    Если вызвать не замоканный запрос, то тест упадет
    Во время мока мы сами определяем ответ
    """
    mocked_request = respx.get('https://httpbin.org/get').respond(json={'test': 'test'})
    result = await fetch_important_data_from_internet()
    assert mocked_request.call_count == 1
    assert result == {'test': 'test'}


@pytest.mark.asyncio()
@patch('my_async_app.some_functions.mock_me', return_value=666)
async def test_fetch_from_async_function(mocked_function: AsyncMock) -> None:
    """
    Используем patch для мока асинхронных функций
    Позиционный аргумент в тесте обязателен, там содержится объект мока
    Из него мы можем вызвать assert_awaited_once() для проверки, что функция была вызвана один и тольо один раз
    """
    result = await fetch_important_data_from_async_function()
    mocked_function.assert_awaited_once()
    assert result == 667


@pytest.mark.asyncio()
@patch.object(NiceClass, '_mock_me_too', return_value=666)
async def test_fetch_from_a_nice_class(mocked_function: AsyncMock) -> None:
    """
    Используем patch для мока асинхронных методов классов
    Позиционный аргумент в тесте всё так же обязателен, там содержится объект мока
    """
    result = await NiceClass().get_nice_number()
    mocked_function.assert_awaited_once()
    assert result == 667


@pytest.mark.asyncio()
async def test_fastapi_app(client: AsyncClient) -> None:
    """
    Используем httpx для тестирования FastAPI приложений
    Это позволяет нам тестировать приложение как в реальной среде
    Мы как бы делаем запрос к нашему приложению, а не к тестируемой функции
    """
    response = await client.get('/')
    assert response.status_code == 200
    assert response.json() == 42
