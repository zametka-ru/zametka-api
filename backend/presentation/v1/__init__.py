from .endpoints import hello

from fastapi import FastAPI


def include_routers(app: FastAPI):
    """Include endpoints APIRouters to the main app"""

    app.include_router(hello.router)
