import datetime
from typing import Optional

import jwt

from fastapi_mail import FastMail
from passlib.context import CryptContext

from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.orm import Session

from starlette.background import BackgroundTasks

from adapters.v1.auth import send_confirm_mail, create_verify_email_token, check_email_verification_token
from adapters.v1.exceptions.auth import JWTAlreadyUsedError, JWTExpiredError

from core.db import User
from core.db.services.users import create_user, make_user_active, get_user_by_email
from core.settings import AuthSettings

from presentation.v1.schemas.auth import (
    RegisterSuccessResponse,
    RegisterFailedResponse,
    VerifyEmailSuccessResponse,
    VerifyEmailFailedResponse,
)


async def register_user(
    user_data: dict,
    background_tasks: BackgroundTasks,
    pwd_context: CryptContext,
    session: Session,
    mail_context: FastMail,
    auth_settings: AuthSettings,
):
    """User register process"""

    user_password: str = user_data.get("password")  # type:ignore

    user_data["password"] = User.hash_password(user_password, pwd_context)
    user_data["joined_at"] = datetime.datetime.utcnow()

    try:
        user: User = await create_user(session, user_data)

        secret_key: str = auth_settings.secret_key
        algorithm: str = auth_settings.algorithm

        token: bytes = create_verify_email_token(secret_key, algorithm, user)

        send_confirm_mail(
            mail_context, user_data.get("email"), background_tasks, str(token)
        )

    except IntegrityError:
        return RegisterFailedResponse(
            details="Такой пользователь уже существует. (Либо что-то пошло не так)"
        )

    except DBAPIError as exc:
        return RegisterFailedResponse(details=str(exc))

    return RegisterSuccessResponse()


async def user_verify_email(token: str, auth_settings: AuthSettings, session: Session):
    auth_settings: AuthSettings  # type:ignore

    secret_key: str = auth_settings.secret_key
    algorithm: str = auth_settings.algorithm

    try:
        payload: dict[str, str | int] = jwt.decode(token, secret_key, algorithm)
        email: Optional[str] = payload.get("email")

        user: User = await get_user_by_email(session, email)

        check_email_verification_token(secret_key, algorithm, user, token)

        await make_user_active(session, user)

    except JWTAlreadyUsedError as exc:
        return VerifyEmailFailedResponse(details=str(exc))

    except JWTExpiredError as exc:
        return VerifyEmailFailedResponse(details=str(exc))

    except jwt.DecodeError:
        return VerifyEmailFailedResponse(details="Error while decoding your token.")

    except DBAPIError as exc:
        return VerifyEmailFailedResponse(details=str(exc))

    return VerifyEmailSuccessResponse(email=payload.get("email"))
