from exception_handlers.script import (
    script_access_denied_exception_handler,
    script_not_exists_exception_handler,
)
from fastapi import FastAPI
from fastapi_another_jwt_auth.exceptions import AuthJWTException
from jwt.exceptions import ExpiredSignatureError
from sqlalchemy.exc import IntegrityError

from yourscript.domain.exceptions.refresh_token import RefreshTokenNotExistsError
from yourscript.domain.exceptions.script import (
    ScriptAccessDeniedError,
    ScriptNotExistsError,
)
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

from .endpoints import auth, script
from .exception_handlers.auth import (
    authjwt_exception_handler,
    corrupted_token_exception_handler,
    expired_token_exception_handler,
    invalid_credentials_exception_handler,
    refresh_not_exists_exception_handler,
    token_already_used_exception_handler,
    unique_exception_handler,
    user_not_active_exception_handler,
    user_not_exists_exception_handler,
    weak_password_exception_handler,
)


def include_routers(app: FastAPI) -> None:
    """Include endpoints APIRouters to the main app"""

    app.include_router(auth.router)
    app.include_router(script.router)


def include_exception_handlers(app: FastAPI) -> None:
    """Include exceptions handlers to the main app"""

    # Auth
    app.add_exception_handler(IntegrityError, unique_exception_handler)
    app.add_exception_handler(WeakPasswordError, weak_password_exception_handler)
    app.add_exception_handler(UserIsNotActiveError, user_not_active_exception_handler)
    app.add_exception_handler(UserIsNotExistsError, user_not_exists_exception_handler)
    app.add_exception_handler(
        InvalidCredentialsError, invalid_credentials_exception_handler
    )
    app.add_exception_handler(ExpiredSignatureError, expired_token_exception_handler)
    app.add_exception_handler(
        TokenAlreadyUsedError, token_already_used_exception_handler
    )
    app.add_exception_handler(
        RefreshTokenNotExistsError, refresh_not_exists_exception_handler
    )
    app.add_exception_handler(
        AuthJWTException,
        authjwt_exception_handler,
    )
    app.add_exception_handler(
        CorruptedTokenError,
        corrupted_token_exception_handler,
    )

    # Script
    app.add_exception_handler(
        ScriptAccessDeniedError, script_access_denied_exception_handler
    )
    app.add_exception_handler(ScriptNotExistsError, script_not_exists_exception_handler)
