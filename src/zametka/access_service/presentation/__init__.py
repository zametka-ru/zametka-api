import logging

from jwt.exceptions import DecodeError

from fastapi import FastAPI
from fastapi_another_jwt_auth.exceptions import AuthJWTException
from jwt.exceptions import ExpiredSignatureError
from sqlalchemy.exc import IntegrityError

from zametka.access_service.domain.exceptions.email_token import (
    CorruptedEmailTokenError,
    EmailTokenAlreadyUsedError,
)
from zametka.access_service.domain.exceptions.user_identity import (
    InvalidCredentialsError,
    UserIsNotActiveError,
    UserIsNotExistsError,
    WeakPasswordError,
    IsNotAuthorizedError,
)

from zametka.access_service.application.common.exceptions import (
    EventIsNotDeliveredError,
)

from .web_api.endpoints import user

from zametka.access_service.presentation.web_api.exception_handlers.auth import (
    authjwt_exception_handler,
    corrupted_token_exception_handler,
    expired_token_exception_handler,
    invalid_credentials_exception_handler,
    token_already_used_exception_handler,
    unique_exception_handler,
    user_not_active_exception_handler,
    user_not_exists_exception_handler,
    weak_password_exception_handler,
    invalid_encoded_token_exception_handler,
    is_not_authorized_exception_handler,
    event_is_not_delivered_exception_handler,
)


def include_routers(app: FastAPI) -> None:
    """Include endpoints APIRouters to the main app"""

    logging.info("Routers was included.")

    app.include_router(user.router)


def include_exception_handlers(app: FastAPI) -> None:
    """Include exceptions handlers to the main app"""

    logging.info("Exception handlers was included.")

    app.add_exception_handler(IntegrityError, unique_exception_handler)
    app.add_exception_handler(WeakPasswordError, weak_password_exception_handler)
    app.add_exception_handler(UserIsNotActiveError, user_not_active_exception_handler)
    app.add_exception_handler(UserIsNotExistsError, user_not_exists_exception_handler)
    app.add_exception_handler(
        InvalidCredentialsError, invalid_credentials_exception_handler
    )
    app.add_exception_handler(ExpiredSignatureError, expired_token_exception_handler)
    app.add_exception_handler(
        EmailTokenAlreadyUsedError, token_already_used_exception_handler
    )
    app.add_exception_handler(
        AuthJWTException,
        authjwt_exception_handler,
    )
    app.add_exception_handler(
        CorruptedEmailTokenError,
        corrupted_token_exception_handler,
    )
    app.add_exception_handler(
        DecodeError,
        invalid_encoded_token_exception_handler,
    )
    app.add_exception_handler(IsNotAuthorizedError, is_not_authorized_exception_handler)
    app.add_exception_handler(
        EventIsNotDeliveredError, event_is_not_delivered_exception_handler
    )
