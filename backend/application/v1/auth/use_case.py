import datetime

from typing import Optional

import jwt

from sqlalchemy.exc import DBAPIError, IntegrityError

from adapters.v1.auth import (
    send_confirm_mail,
    create_verify_email_token,
    check_email_verification_token,
)
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

from .dto import RegisterInputDTO, VerificationInputDTO


async def register_user(dto: RegisterInputDTO):
    """User register process"""

    user_password: str = dto.user_data.get("password")  # type:ignore

    dto.user_data["password"] = User.hash_password(user_password, dto.pwd_context)
    dto.user_data["joined_at"] = datetime.datetime.utcnow()

    try:
        user: User = await create_user(dto.session, dto.user_data)

        secret_key: str = dto.auth_settings.secret_key
        algorithm: str = dto.auth_settings.algorithm

        token: bytes = create_verify_email_token(secret_key, algorithm, user)

        send_confirm_mail(
            dto.mail_context, dto.user_data.get("email"), dto.background_tasks, str(token)
        )

    except IntegrityError:
        return RegisterFailedResponse(
            details="Такой пользователь уже существует. (Либо что-то пошло не так)"
        )

    except DBAPIError as exc:
        return RegisterFailedResponse(details=str(exc))

    return RegisterSuccessResponse()


async def user_verify_email(dto: VerificationInputDTO):
    auth_settings: AuthSettings  # type:ignore

    secret_key: str = dto.auth_settings.secret_key
    algorithm: str = dto.auth_settings.algorithm

    try:
        payload: dict[str, str | int | bool] = jwt.decode(dto.token, secret_key, algorithm)
        email: Optional[str] = payload.get("email")  # type:ignore

        user: User = await get_user_by_email(dto.session, email)

        check_email_verification_token(secret_key, algorithm, user, dto.token)

        await make_user_active(dto.session, user)

    except JWTAlreadyUsedError as exc:
        return VerifyEmailFailedResponse(details=str(exc))

    except JWTExpiredError as exc:
        return VerifyEmailFailedResponse(details=str(exc))

    except jwt.DecodeError:
        return VerifyEmailFailedResponse(details="Error while decoding your token.")

    except DBAPIError as exc:
        return VerifyEmailFailedResponse(details=str(exc))

    return VerifyEmailSuccessResponse(email=payload.get("email"))
