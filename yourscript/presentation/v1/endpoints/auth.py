from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from starlette.background import BackgroundTasks

from adapters.v1.auth.mailer import ConfirmationTokenMailer
from infrastructure.settings import load_authjwt_settings, AuthJWTSettings

from infrastructure.dependencies import (
    MailDependency,
    AuthSettingsDependency,
    AuthRepositoryDependency,
    UnitOfWorkDependency,
    CryptContextDependency,
    JinjaDependency,
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
)

from application.v1.auth.interfaces import JWTOpsInterface

from infrastructure.db.repositories import AuthRepository
from infrastructure.db.repositories import UnitOfWork

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
    pwd_context: CryptContextDependency = Depends(),
    auth_settings: AuthSettingsDependency = Depends(),
    repository: AuthRepositoryDependency = Depends(),
    mail_context: MailDependency = Depends(),
    uow: UnitOfWorkDependency = Depends(),
    jinja: JinjaDependency = Depends(),
    jwtops: JWTOpsInterface = Depends(),
):
    """Register endpoint"""

    dto = RegisterInputDTO(
        user_email=register_data.email,
        user_password=register_data.password,
        user_first_name=register_data.first_name,
        user_last_name=register_data.last_name,
    )

    mailer = ConfirmationTokenMailer(
        background_tasks=background_tasks, mail=mail_context, jinja=jinja
    )

    response = await register_user(
        dto=dto,
        repository=repository,
        pwd_context=pwd_context,
        token_sender=mailer,
        auth_settings=auth_settings,
        uow=uow,
        jwtops=jwtops,
    )

    return response


@router.get("/verify/{token}")
async def verify_email(
    token: str,
    auth_settings: AuthSettingsDependency = Depends(),
    repository: AuthRepositoryDependency = Depends(),
    uow: UnitOfWorkDependency = Depends(),
    jwtops: JWTOpsInterface = Depends(),
):
    """Email verification endpoint"""

    repository: AuthRepository  # type:ignore
    uow: UnitOfWork  # type:ignore

    dto = VerificationInputDTO(token=token)

    response = await user_verify_email(
        dto=dto,
        repository=repository,
        auth_settings=auth_settings,
        uow=uow,
        jwtops=jwtops,
    )

    return response


@router.post("/login")
async def login(
    user_login: UserLoginSchema,
    Authorize: AuthJWT = Depends(),
    repository: AuthRepositoryDependency = Depends(),
    pwd_context: CryptContextDependency = Depends(),
    uow: UnitOfWorkDependency = Depends(),
):
    """Login endpoint"""

    repository: AuthRepository  # type:ignore
    uow: UnitOfWork  # type:ignore

    dto = LoginInputDTO(
        user_email=user_login.email,
        user_password=user_login.password,
    )

    response = await user_login_case(
        dto=dto,
        repository=repository,
        Authorize=Authorize,
        pwd_context=pwd_context,
        uow=uow,
    )

    return response


@router.post("/refresh")
async def refresh(
    Authorize: AuthJWT = Depends(),
    repository: AuthRepositoryDependency = Depends(),
    uow: UnitOfWorkDependency = Depends(),
):
    """Refresh access token endpoint"""

    Authorize.jwt_refresh_token_required()

    return await token_refresh(Authorize=Authorize, repository=repository, uow=uow)
