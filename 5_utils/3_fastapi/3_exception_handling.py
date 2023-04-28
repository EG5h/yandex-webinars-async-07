import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class CatException(Exception):
    def __init__(self, name: str):
        self.name = name


app = FastAPI()


@app.exception_handler(CatException)
async def cat_exception_handler(request: Request, exc: CatException) -> JSONResponse:
    return JSONResponse(
        status_code=418,
        content={'message': f'Oops! {exc.name} did something. There goes a rainbow...'},
    )


@app.get('/cats/{name}')
async def read_cat(name: str) -> dict[str, str]:
    if name == 'yolo':
        raise CatException(name=name)
    return {'cat_name': name}


if __name__ == '__main__':
    uvicorn.run(app)
