from fastapi import FastAPI

from my_async_app.more_functions import mock_me

app = FastAPI()


@app.get("/")
async def root() -> int:
    return await mock_me()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
