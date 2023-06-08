from fastapi.responses import JSONResponse
from fastapi import Request, FastAPI

from sqlalchemy.exc import IntegrityError, DBAPIError


def value_error(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"details": str(exc)})


def integrity_error(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=400,
        content={
            "details": "Такая запись уже существует (Либо нарушение целостности БД)"
        },
    )


def db_api_error(request: Request, exc: DBAPIError):
    print(exc)
    return JSONResponse(
        status_code=400,
        content={"details": "Ошибка базы данных! Проверьте правильность данных!"},
    )


def include(app: FastAPI) -> None:
    """Include auth exception handlers"""

    app.exception_handler(IntegrityError)(integrity_error)
    app.exception_handler(DBAPIError)(db_api_error)
    app.exception_handler(ValueError)(value_error)
