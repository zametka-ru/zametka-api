import datetime
import jwt

from typing import Optional


from .logic import (
    send_confirm_mail,
    create_verify_email_token,
    check_email_verification_token,
)

from domain.v1.auth import validate_password

from domain.db import User

from .responses import (
    RegisterSuccessResponse,
    VerifyEmailSuccessResponse,
    LoginSuccessResponse,
    RefreshSuccessResponse,
)

from .dto import RegisterInputDTO, VerificationInputDTO, LoginInputDTO

from adapters.repository.auth import AuthRepository

from adapters.repository.uow import UnitOfWork

from fastapi_jwt_auth import AuthJWT
from fastapi_mail import FastMail
from passlib.context import CryptContext
from starlette.background import BackgroundTasks

from core.settings import AuthSettings


async def register_user(
    dto: RegisterInputDTO,
    repository: AuthRepository,
    background_tasks: BackgroundTasks,
    pwd_context: CryptContext,
    mail_context: FastMail,
    auth_settings: AuthSettings,
    uow: UnitOfWork,
):
    """User register process"""

    user_password: str = dto.user_password

    validate_password(user_password)

    dto.user_password = User.hash_password(user_password, pwd_context)
    user_joined_at = datetime.datetime.utcnow()

    user: User = await repository.create_user(
        email=dto.user_email,
        password=dto.user_password,
        first_name=dto.user_first_name,
        last_name=dto.user_last_name,
        joined_at=user_joined_at,
    )

    await uow.commit()

    secret_key: str = auth_settings.secret_key
    algorithm: str = auth_settings.algorithm

    token: bytes = create_verify_email_token(secret_key, algorithm, user)

    send_confirm_mail(
        mail_context,
        dto.user_email,
        background_tasks,
        str(token),
    )

    return RegisterSuccessResponse()


async def user_verify_email(
    dto: VerificationInputDTO,
    repository: AuthRepository,
    auth_settings: AuthSettings,
    uow: UnitOfWork,
):
    auth_settings: AuthSettings  # type:ignore

    secret_key: str = auth_settings.secret_key
    algorithm: str = auth_settings.algorithm

    payload: dict[str, str | int | bool] = jwt.decode(dto.token, secret_key, algorithm)

    user_id: Optional[int] = payload.get("id")  # type:ignore

    user: User = await repository.get_user_by_id(user_id)

    check_email_verification_token(secret_key, algorithm, user, dto.token)

    await repository.make_user_active(user)

    await uow.commit()

    return VerifyEmailSuccessResponse(user_id=payload.get("id"))  # type:ignore


async def user_login(
    dto: LoginInputDTO,
    repository: AuthRepository,
    Authorize: AuthJWT,
    pwd_context: CryptContext,
):
    """Login user"""

    user: User = await repository.get_user_by_email(dto.user_email)

    if not user:
        raise ValueError(f"There is no users with id\n{dto.user_email}")

    if not user.is_active:
        raise ValueError("Confirm your email first, or you was banned :)")

    if not user.compare_passwords(dto.user_password, pwd_context):
        raise ValueError("Invalid credentials (check your password)")

    access_token = Authorize.create_access_token(subject=user.id)  # type:ignore
    refresh_token = Authorize.create_refresh_token(subject=user.id)  # type:ignore

    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)

    return LoginSuccessResponse()


async def token_refresh(Authorize: AuthJWT):
    """Refresh user access token"""

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)

    Authorize.set_access_cookies(new_access_token)

    return RefreshSuccessResponse()
