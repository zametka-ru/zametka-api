import uvicorn

from fastapi import FastAPI

from v1 import include_routers

from core.settings import load_settings
from core.db import get_session, get_async_sessionmaker

from sqlalchemy.orm import Session

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    settings = load_settings()
    async_sessionmaker = await get_async_sessionmaker(settings)

    app.dependency_overrides[Session] = lambda: get_session(async_sessionmaker)

    include_routers(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=80)
