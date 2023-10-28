from typing import Optional

from datetime import timedelta, datetime

from infrastructure.db import User

from application.v1.exceptions.auth import JWTAlreadyUsedError, JWTExpiredError

from .interfaces import JWTOpsInterface



def jwt_already_used_check(
    secret_key: str, algorithm: str, user: User, token: str, jwtops: JWTOpsInterface
) -> None:
    """
    Compares JWT tokens

    :param jwtops: JWT operations object
    :param token: token
    :param user: User which need email verification
    :param secret_key: random hex for signing JWT
    :param algorithm: algorithm for signing JWT
    :return: None: may raise JWTAlreadyUsedError
    """

    token_payload: JWTPayload = jwtops.decode(token, secret_key, algorithm)

    token_user_is_active: bool = token_payload.get("user_is_active")  # type:ignore

    if user.is_active != token_user_is_active:
        raise JWTAlreadyUsedError()
