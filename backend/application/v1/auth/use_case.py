import datetime
import jwt

from typing import Optional

from adapters.repository.uow import UnitOfWork
from core.dependencies import (
    AuthSettingsDependency,
    CryptContextDependency,
    AuthJWTDependency,
)

from .interfaces import MailTokenSenderInterface, JWTOpsInterface

from .logic import (
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

from core.settings import AuthSettings


async def register_user(
    dto: RegisterInputDTO,
    repository: AuthRepository,
    pwd_context: CryptContextDependency,
    token_sender: MailTokenSenderInterface,
    auth_settings: AuthSettingsDependency,
    uow: UnitOfWork,
    jwtops: JWTOpsInterface,
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

    token: str = create_verify_email_token(secret_key, algorithm, user, jwtops)

    token_sender.send(
        token, subject="Завершите регистрацию в yourscript.", to_email=dto.user_email
    )

    return RegisterSuccessResponse()


async def user_verify_email(
    dto: VerificationInputDTO,
    repository: AuthRepository,
    auth_settings: AuthSettingsDependency,
    uow: UnitOfWork,
    jwtops: JWTOpsInterface,
):
    auth_settings: AuthSettings  # type:ignore

    secret_key: str = auth_settings.secret_key
    algorithm: str = auth_settings.algorithm

    payload: dict[str, str | int | bool] = jwt.decode(dto.token, secret_key, algorithm)

    user_id: Optional[int] = payload.get("id")  # type:ignore

    user: User = await repository.get_user_by_id(user_id)

    check_email_verification_token(secret_key, algorithm, user, dto.token, jwtops)

    await repository.make_user_active(user)

    await uow.commit()

    return VerifyEmailSuccessResponse(user_id=payload.get("id"))  # type:ignore


async def user_login(
    dto: LoginInputDTO,
    repository: AuthRepository,
    Authorize: AuthJWTDependency,
    pwd_context: CryptContextDependency,
    uow: UnitOfWork,
):
    """Login user"""

    user: User = await repository.get_user_by_email(dto.user_email)

    if not user:
        raise ValueError(f"There is no users with email \n{dto.user_email}")

    if not user.is_active:
        raise ValueError("Confirm your email first, or you was banned :)")

    if not user.compare_passwords(dto.user_password, pwd_context):
        raise ValueError("Invalid credentials (check your password)")

    access_token = Authorize.create_access_token(subject=user.id)  # type:ignore
    refresh_token = Authorize.create_refresh_token(subject=user.id)  # type:ignore

    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)

    await repository.delete_user_tokens(user.id)  # type:ignore
    await repository.create_refresh_token(user.id, refresh_token)  # type:ignore

    await uow.commit()

    return LoginSuccessResponse()


async def token_refresh(
    Authorize: AuthJWTDependency, repository: AuthRepository, uow: UnitOfWork
):
    """Refresh user access token"""

    refresh_exists = await repository.is_token_exists(Authorize._token)

    if not refresh_exists:
        raise ValueError("Invalid refresh token")

    current_user: int = Authorize.get_jwt_subject()

    user: User = await repository.get_user_by_id(current_user)

    new_access_token = Authorize.create_access_token(subject=current_user)
    new_refresh_token = Authorize.create_refresh_token(subject=current_user)

    Authorize.set_access_cookies(new_access_token)
    Authorize.set_refresh_cookies(new_refresh_token)

    await repository.delete_user_tokens(user.id)  # type:ignore
    await repository.create_refresh_token(user.id, new_refresh_token)  # type:ignore

    await uow.commit()

    return RefreshSuccessResponse()
