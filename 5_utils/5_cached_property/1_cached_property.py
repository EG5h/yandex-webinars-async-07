import asyncio

from cached_property import cached_property


class MyClass:

    async def get_data(self):
        print('get_data called ')
        return await self._my_property

    @cached_property
    async def _my_property(self):
        print('my_property called')
        await asyncio.sleep(0.5)
        return 42


async def main():
    obj = MyClass()
    await asyncio.gather(*(obj.get_data() for _ in range(5)))
    # print(await obj.get_data())
    # print(await obj.get_data())


if __name__ == '__main__':
    asyncio.run(main())
