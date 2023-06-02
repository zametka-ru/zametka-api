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
    UnitOfWorkDependency,
)

from application.v1.auth.use_case import (
    register_user,
    user_verify_email,
    user_login as user_login_case,
    token_refresh,
)
from application.v1.auth.dto import (
    RegisterInputDTO,
    VerificationInputDTO,
    LoginInputDTO,
    RefreshInputDTO,
)

from adapters.repository import AuthRepository, UnitOfWork

from ..schemas.auth import (
    UserRegisterSchema,
    UserLoginSchema,
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
    uow: UnitOfWorkDependency = Depends(),
):
    """Register endpoint"""

    mail_context: FastMail  # type:ignore
    auth_settings: AuthSettings  # type:ignore
    repository: AuthRepository  # type:ignore
    uow: UnitOfWork  # type:ignore

    register_data_dict: dict = register_data.dict()

    dto = RegisterInputDTO(
        user_data=register_data_dict,
        background_tasks=background_tasks,
        pwd_context=pwd_context,
        mail_context=mail_context,
        auth_settings=auth_settings,
        uow=uow,
    )

    response = await register_user(dto, repository)

    return response


@router.get("/verify/{token}")
async def verify_email(
    token: str,
    auth_settings: AuthSettingsDependency = Depends(),
    repository: AuthRepositoryDependency = Depends(),
    uow: UnitOfWorkDependency = Depends(),
):
    """Email verification endpoint"""

    auth_settings: AuthSettings  # type:ignore
    repository: AuthRepository  # type:ignore
    uow: UnitOfWork  # type:ignore

    dto = VerificationInputDTO(token=token, auth_settings=auth_settings, uow=uow)

    return await user_verify_email(dto, repository)


@router.post("/login")
async def login(
    user_login: UserLoginSchema,
    Authorize: AuthJWT = Depends(),
    repository: AuthRepositoryDependency = Depends(),
    pwd_context: CryptContext = Depends(),
):
    """Login endpoint"""

    repository: AuthRepository  # type:ignore

    dto = LoginInputDTO(
        user_login=user_login, Authorize=Authorize, pwd_context=pwd_context
    )

    return await user_login_case(dto, repository)


@router.post("/refresh")
async def refresh(Authorize: AuthJWT = Depends()):
    """Refresh access token endpoint"""

    Authorize.jwt_refresh_token_required()

    dto = RefreshInputDTO(
        Authorize=Authorize,
    )

    return await token_refresh(dto)
