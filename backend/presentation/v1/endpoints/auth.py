from fastapi import APIRouter, Depends

from fastapi_jwt_auth import AuthJWT
from fastapi_mail import FastMail
from passlib.context import CryptContext
from starlette.background import BackgroundTasks

from core.settings import load_authjwt_settings, AuthJWTSettings, AuthSettings
from core.dependencies import (
    MailDependency,
    AuthSettingsDependency,
    AuthRepositoryDependency,
)

from application.v1.auth.use_case import register_user, user_verify_email
from application.v1.auth.dto import RegisterInputDTO, VerificationInputDTO

from repository import AuthRepository

from ..schemas.auth import (
    UserRegisterSchema,
)

router = APIRouter(
    prefix="/v1/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@AuthJWT.load_config
def load_settings() -> AuthJWTSettings:
    """Load settings for AuthJWT"""

    return load_authjwt_settings()


@router.post("/register")
async def register(
    register_data: UserRegisterSchema,
    background_tasks: BackgroundTasks,
    pwd_context: CryptContext = Depends(),
    auth_settings: AuthSettingsDependency = Depends(),
    repository: AuthRepositoryDependency = Depends(),
    mail_context: MailDependency = Depends(),
):
    mail_context: FastMail  # type:ignore
    auth_settings: AuthSettings  # type:ignore
    repository: AuthRepository  # type:ignore

    register_data_dict: dict = register_data.dict()

    dto = RegisterInputDTO(
        user_data=register_data_dict,
        background_tasks=background_tasks,
        pwd_context=pwd_context,
        mail_context=mail_context,
        auth_settings=auth_settings,
        repository=repository,
    )

    response = await register_user(dto)

    return response


@router.get("/verify/{token}")
async def verify_email(
    token: str,
    auth_settings: AuthSettingsDependency = Depends(),
    repository: AuthRepositoryDependency = Depends(),
):
    auth_settings: AuthSettings  # type:ignore
    repository: AuthRepository  # type:ignore

    dto = VerificationInputDTO(
        token=token,
        auth_settings=auth_settings,
        repository=repository,
    )

    return await user_verify_email(dto)


@router.post("/refresh")
async def refresh(Authorize: AuthJWT = Depends()):
    """Refresh JWT"""

    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)

    return {"access_token": new_access_token}
