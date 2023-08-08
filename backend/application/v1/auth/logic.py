from typing import Optional

from datetime import timedelta, datetime

from domain.db import User

from application.v1.exceptions.auth import JWTAlreadyUsedError, JWTExpiredError

from .interfaces import JWTOpsInterface


def create_verify_email_token(
    secret_key: str,
    algorithm: str,
    user: User,
    jwtops: JWTOpsInterface,
    utcnow: Optional[datetime | str] = None,
    expires: int = 15,
) -> str:
    """
    Create the email-verification jwt token.

    :param jwtops: JWT operations object
    :param utcnow: time-signing for token, maybe None
    :param user: User which need email verification
    :param secret_key: random hex for signing JWT
    :param algorithm: algorithm for signing JWT
    :param expires: token expires in minutes
    :return: str: JWT token
    """

    if utcnow is None:
        utcnow: datetime = datetime.utcnow()  # type:ignore

    payload = {
        "id": user.id,
        "expires": expires,
        "user_is_active": user.is_active,
        "utcnow": str(utcnow),
    }

    token: str = jwtops.encode(payload, secret_key, algorithm)

    return token


JWTPayload = dict[str, int | str | bool]


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


def jwt_expired_check(token_payload: dict[str, int | str]) -> None:
    """
    Check is JWT expired

    May raise JWTExpiredError
    """

    expires: int = token_payload.get("expires")  # type:ignore
    expires_delta: timedelta = timedelta(minutes=expires)

    token_utcnow: str = token_payload.get("utcnow")  # type:ignore
    token_utcnow_normalized = token_utcnow.split(".")[0]

    token_utcnow_datetime: datetime = datetime.fromisoformat(token_utcnow_normalized)

    utcnow = datetime.utcnow()

    token_expire_time: datetime = token_utcnow_datetime + expires_delta

    if utcnow > token_expire_time:
        raise JWTExpiredError()


def check_email_verification_token(
    secret_key: str, algorithm: str, user: User, token: str, jwtops: JWTOpsInterface
) -> None:
    """
    Check the email verification token by 2-step check:

    1. Check token not used second-time
    2. Check token not exceeded expires-time

    :param jwtops: JWT Operations object
    :param secret_key: secret key for signing JWT
    :param algorithm: algorithm for signing JWT
    :param user: user which need email verification
    :param token: other token to token-compare check
    :param expires: token expire time in minutes
    :return None: may raise JWTAlreadyUsedError or JWTExpiredError
    """

    jwt_already_used_check(secret_key, algorithm, user, token, jwtops=jwtops)

    token_payload = jwtops.decode(token, secret_key, algorithm)

    jwt_expired_check(token_payload)
