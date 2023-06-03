import datetime
import jwt


from typing import Optional

from sqlalchemy.exc import DBAPIError, IntegrityError

from adapters.v1.auth import (
    send_confirm_mail,
    create_verify_email_token,
    check_email_verification_token,
)
from adapters.v1.exceptions.auth import JWTCheckError

from core.db import User
from core.settings import AuthSettings

from presentation.v1.schemas.auth import (
    RegisterSuccessResponse,
    RegisterFailedResponse,
    VerifyEmailSuccessResponse,
    VerifyEmailFailedResponse,
    LoginSuccessResponse,
    LoginFailedResponse,
    RefreshSuccessResponse,
)

from .dto import RegisterInputDTO, VerificationInputDTO, LoginInputDTO, RefreshInputDTO

from adapters.repository.auth import AuthRepository


async def register_user(dto: RegisterInputDTO, repository: AuthRepository):
    """User register process"""

    user_password: str = dto.user_data.get("password")  # type:ignore

    dto.user_data["password"] = User.hash_password(user_password, dto.pwd_context)
    dto.user_data["joined_at"] = datetime.datetime.utcnow()

    try:
        user: User = await repository.create_user(dto.user_data)
        await dto.uow.commit()

        secret_key: str = dto.auth_settings.secret_key
        algorithm: str = dto.auth_settings.algorithm

        token: bytes = create_verify_email_token(secret_key, algorithm, user)

        send_confirm_mail(
            dto.mail_context,
            dto.user_data.get("email"),
            dto.background_tasks,
            str(token),
        )

    except IntegrityError:
        return RegisterFailedResponse(
            details="This user already exists (or something wrong)"
        )

    except DBAPIError as exc:
        return RegisterFailedResponse(details=str(exc))
    return RegisterSuccessResponse()


async def user_verify_email(dto: VerificationInputDTO, repository: AuthRepository):
    auth_settings: AuthSettings  # type:ignore

    secret_key: str = dto.auth_settings.secret_key
    algorithm: str = dto.auth_settings.algorithm

    try:
        payload: dict[str, str | int | bool] = jwt.decode(
            dto.token, secret_key, algorithm
        )
        email: Optional[str] = payload.get("email")  # type:ignore

        user: User = await repository.get_user_by_email(email)

        check_email_verification_token(secret_key, algorithm, user, dto.token)

        await repository.make_user_active(user)

        await dto.uow.commit()

    except JWTCheckError as exc:
        return VerifyEmailFailedResponse(details=str(exc))

    except jwt.DecodeError:
        return VerifyEmailFailedResponse(details="Error while decoding your token.")

    except DBAPIError as exc:
        return VerifyEmailFailedResponse(details=str(exc))

    return VerifyEmailSuccessResponse(email=payload.get("email"))


async def user_login(dto: LoginInputDTO, repository: AuthRepository):
    """Login user"""

    user: User = await repository.get_user_by_email(dto.user_login.email)

    if not user:
        return LoginFailedResponse(
            details=f"There is no users with email\n{dto.user_login.email}"
        )

    if not user.is_active:
        return LoginFailedResponse(
            details="Confirm your email first, or you was banned :)"
        )

    if not user.compare_passwords(dto.user_login.password, dto.pwd_context):
        return LoginFailedResponse(details="Invalid credentials (check your password)")

    access_token = dto.Authorize.create_access_token(subject=dto.user_login.email)
    refresh_token = dto.Authorize.create_refresh_token(subject=dto.user_login.email)

    return LoginSuccessResponse(access_token=access_token, refresh_token=refresh_token)


async def token_refresh(dto: RefreshInputDTO):
    """Refresh user access token"""

    current_user = dto.Authorize.get_jwt_subject()
    new_access_token = dto.Authorize.create_access_token(subject=current_user)

    return RefreshSuccessResponse(access_token=new_access_token)
