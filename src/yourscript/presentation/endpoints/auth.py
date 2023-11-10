from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi_another_jwt_auth import AuthJWT

from yourscript.application.auth.email_verification import (
    EmailVerificationInputDTO,
    EmailVerificationOutputDTO,
)
from yourscript.application.auth.refresh_token import (
    RefreshTokenInputDTO,
    RefreshTokenOutputDTO,
)
from yourscript.application.auth.sign_in import SignInInputDTO, SignInOutputDTO
from yourscript.application.auth.sign_up import SignUpInputDTO, SignUpOutputDTO
from yourscript.domain.entities.refresh_token import RefreshToken
from yourscript.domain.value_objects.user_id import UserId
from yourscript.presentation.interactor_factory import InteractorFactory
from yourscript.presentation.schemas.auth import UserLoginSchema, UserRegisterSchema

router = APIRouter(
    prefix="/v1/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/sign-up", response_model=SignUpOutputDTO)
async def sign_up(
    user_data: UserRegisterSchema,
    background_tasks: BackgroundTasks,
    ioc: InteractorFactory = Depends(),
):
    """Register endpoint"""

    async with ioc.sign_up(background_tasks=background_tasks) as interactor:
        response = await interactor(
            SignUpInputDTO(
                user_email=user_data.email,
                user_password=user_data.password,
                user_first_name=user_data.first_name,
                user_last_name=user_data.last_name,
            )
        )

        return response


@router.post("/sign-in", response_model=SignInOutputDTO)
async def sign_in(
    auth_data: UserLoginSchema,
    jwt: AuthJWT = Depends(),
    ioc: InteractorFactory = Depends(),
):
    """Login endpoint"""

    async with ioc.sign_in(jwt) as interactor:
        response = await interactor(
            SignInInputDTO(email=auth_data.email, password=auth_data.password)
        )

    jwt.set_access_cookies(response.access)
    jwt.set_refresh_cookies(response.refresh)

    return response


@router.get("/verify/{token}", response_model=EmailVerificationOutputDTO)
async def email_verification(token: str, ioc: InteractorFactory = Depends()):
    """Email verification endpoint"""

    async with ioc.email_verification() as interactor:
        response = await interactor(
            EmailVerificationInputDTO(
                token=token,
            )
        )

        return response


@router.post("/refresh", response_model=RefreshTokenOutputDTO)
async def refresh_token(
    jwt: AuthJWT = Depends(),
    ioc: InteractorFactory = Depends(),
):
    """Refresh access token endpoint"""

    jwt.jwt_refresh_token_required()

    user_id: UserId = UserId(int(jwt.get_jwt_subject()))

    async with ioc.refresh_token(jwt) as interactor:
        response = await interactor(
            RefreshTokenInputDTO(
                refresh=RefreshToken(token=jwt._token, user_id=user_id),
            )
        )

    jwt.set_access_cookies(response.access)
    jwt.set_refresh_cookies(response.refresh)

    return response
