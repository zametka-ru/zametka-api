import datetime
import jwt

from typing import Optional

from infrastructure.db.repositories import UnitOfWork
from infrastructure.stubs import (
    AuthSettingsStub,
    CryptContextStub,
    AuthJWTStub,
)

from .interfaces import MailTokenSenderInterface, JWTOpsInterface

from .logic import (
    create_verify_email_token,
    check_email_verification_token,
)

from infrastructure.db import User

from .responses import (
    RegisterSuccessResponse,
    VerifyEmailSuccessResponse,
    LoginSuccessResponse,
    RefreshSuccessResponse,
)

from .dto import RegisterInputDTO, VerificationInputDTO, LoginInputDTO

from infrastructure.db.repositories import AuthRepository

from infrastructure.settings import AuthSettings



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
