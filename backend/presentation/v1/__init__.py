from .endpoints import auth
from .endpoints import script

from .exception_handlers import auth as auth_exception_handlers

from fastapi import FastAPI


def include_routers(app: FastAPI) -> None:
    """Include endpoints APIRouters to the main app"""

    app.include_router(auth.router)
    app.include_router(script.router)


def include_exception_handlers(app: FastAPI) -> None:
    """Include exceptions handlers to the main app"""

    auth_exception_handlers.include(app)
