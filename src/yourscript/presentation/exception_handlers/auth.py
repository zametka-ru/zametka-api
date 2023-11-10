from asyncpg import UniqueViolationError
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi_another_jwt_auth.exceptions import AuthJWTException
from jwt.exceptions import ExpiredSignatureError

from yourscript.domain.exceptions.refresh_token import RefreshTokenNotExistsError
from yourscript.domain.exceptions.token import (
    CorruptedTokenError,
    TokenAlreadyUsedError,
)
from yourscript.domain.exceptions.user import (
    InvalidCredentialsError,
    UserIsNotActiveError,
    UserIsNotExistsError,
    WeakPasswordError,
)


async def unique_exception_handler(_request: Request, _exc: UniqueViolationError):
    return JSONResponse(
        status_code=422,
        content={"message": "Такая запись уже существует!"},
    )


async def weak_password_exception_handler(_request: Request, exc: WeakPasswordError):
    return JSONResponse(
        status_code=422,
        content={"message": f"Слабый пароль! {exc.message}"},
    )


async def user_not_active_exception_handler(
    _request: Request, _exc: UserIsNotActiveError
):
    return JSONResponse(
        status_code=422,
        content={
            "message": "Пользователь не активен. Сначала вы должны верифицировать свою почту."
        },
    )


async def user_not_exists_exception_handler(
    _request: Request, _exc: UserIsNotExistsError
):
    return JSONResponse(
        status_code=404,
        content={"message": "Пользователя не существует."},
    )


async def invalid_credentials_exception_handler(
    _request: Request, _exc: InvalidCredentialsError
):
    return JSONResponse(
        status_code=422,
        content={"message": "Неправильно введены данные для входа!"},
    )


async def refresh_not_exists_exception_handler(
    _request: Request, _exc: RefreshTokenNotExistsError
):
    return JSONResponse(
        status_code=404,
        content={"message": "Такого refresh-токена не существует!"},
    )


async def expired_token_exception_handler(
    _request: Request, _exc: ExpiredSignatureError
):
    return JSONResponse(
        status_code=408,
        content={"message": "Токен истёк."},
    )


async def corrupted_token_exception_handler(
    _request: Request, _exc: CorruptedTokenError
):
    return JSONResponse(
        status_code=422,
        content={"message": "Токен повреждён."},
    )


async def token_already_used_exception_handler(
    _request: Request, _exc: TokenAlreadyUsedError
):
    return JSONResponse(
        status_code=422,
        content={"message": "Токен уже использован."},
    )


def authjwt_exception_handler(_request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,  # type:ignore
        content={"detail": exc.message},  # type:ignore
    )
