from .endpoints import hello

from fastapi import FastAPI


def include_routers(app: FastAPI) -> None:
    app.include_router(hello.router)
