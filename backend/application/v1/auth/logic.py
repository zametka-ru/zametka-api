import jwt

from typing import Optional

from datetime import timedelta, datetime

from fastapi_mail import FastMail, MessageSchema, MessageType
from starlette.background import BackgroundTasks

from core.db import User

from application.v1.exceptions.auth import JWTAlreadyUsedError, JWTExpiredError


def send_confirm_mail(
    mail: FastMail, user_email: str, background_tasks: BackgroundTasks, token: str
):
    """Send confirmation email after register user"""

    html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> """

    message = MessageSchema(
        subject=f"Ваш токен для подтверждения почты {token}",
        recipients=[user_email],
        body=html,
        subtype=MessageType.html,
    )

    background_tasks.add_task(mail.send_message, message)


def create_verify_email_token(
    secret_key: str,
    algorithm: str,
    user: User,
    utcnow: Optional[datetime | str] = None,
    expires: int = 15,
) -> bytes:
    """
    Create the email-verification jwt token.

    :param utcnow: time-signing for token, maybe None
    :param user: User which need email verification
    :param secret_key: random hex for signing JWT
    :param algorithm: algorithm for signing JWT
    :param expires: token expires in minutes
    :return: bytes: JWT token
    """

    if utcnow is None:
        utcnow: datetime = datetime.utcnow()  # type:ignore

    payload = {
        "email": user.email,
        "expires": expires,
        "user_is_active": user.is_active,
        "utcnow": str(utcnow),
    }

    token: bytes = jwt.encode(payload, secret_key, algorithm)

    return token


JWTPayload = dict[str, int | str | bool]


def jwt_already_used_check(
    secret_key: str,
    algorithm: str,
    user: User,
    token: str,
) -> None:
    """
    Compares JWT tokens

    :param token: token
    :param user: User which need email verification
    :param secret_key: random hex for signing JWT
    :param algorithm: algorithm for signing JWT
    :return: None: may raise JWTAlreadyUsedError
    """

    token_payload: JWTPayload = jwt.decode(token, secret_key, algorithm)

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
    secret_key: str, algorithm: str, user: User, token: str
) -> None:
    """
    Check the email verification token by 2-step check:

    1. Check token not used second-time
    2. Check token not exceeded expires-time

    :param secret_key: secret key for signing JWT
    :param algorithm: algorithm for signing JWT
    :param user: user which need email verification
    :param token: other token to token-compare check
    :param expires: token expire time in minutes
    :return None: may raise JWTAlreadyUsedError or JWTExpiredError
    """

    jwt_already_used_check(secret_key, algorithm, user, token)

    token_payload = jwt.decode(token, secret_key, algorithm)

    jwt_expired_check(token_payload)


def validate_password(password: str) -> None:
    """Validate password (business logic), may raise ValueError"""

    error_messages = {
        "Password must contain an uppercase letter.": lambda s: any(
            x.isupper() for x in s
        ),
        "Password must contain a lowercase letter.": lambda s: any(
            x.islower() for x in s
        ),
        "Password must contain a digit.": lambda s: any(x.isdigit() for x in s),
        "Password cannot contain white spaces.": lambda s: not any(
            x.isspace() for x in s
        ),
    }

    for message, password_validator in error_messages.items():
        if not password_validator(password):
            raise ValueError(message)
