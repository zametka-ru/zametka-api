from fastapi import APIRouter, Depends

from application.common.adapters import JWT

from application.auth.sign_up import SignUpInputDTO
from application.auth.sign_in import SignInInputDTO
from application.auth.email_verification import EmailVerificationInputDTO
from application.auth.refresh_token import RefreshTokenInputDTO
from domain.value_objects.user_id import UserId

from presentation.interactor_factory import InteractorFactory
from presentation.schemas.auth import (
    UserRegisterSchema,
    UserLoginSchema,
)

router = APIRouter(
    prefix="/v1/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/sign-up")
async def sign_up(
        user_data: UserRegisterSchema,
        ioc: InteractorFactory = Depends(),
):
    """Register endpoint"""

    async with ioc.sign_up() as interactor:
        response = await interactor(SignUpInputDTO(
            user_email=user_data.email,
            user_password=user_data.password,
            user_first_name=user_data.first_name,
            user_last_name=user_data.last_name,
        ))

        return response


@router.post("/sign-in")
async def sign_in(
        auth_data: UserLoginSchema,
        jwt: JWT = Depends(),
        ioc: InteractorFactory = Depends(),
):
    """Login endpoint"""

    async with ioc.sign_in(jwt) as interactor:
        response = await interactor(SignInInputDTO(
            email=auth_data.email,
            password=auth_data.password
        ))

        return response


@router.get("/verify/{token}")
async def email_verification(token: str, ioc: InteractorFactory = Depends()):
    """Email verification endpoint"""

    async with ioc.email_verification() as interactor:
        response = await interactor(EmailVerificationInputDTO(
            token=token,
        ))

        return response


@router.post("/refresh")
async def refresh_token(
        jwt: JWT = Depends(),
        ioc: InteractorFactory = Depends(),
):
    """Refresh access token endpoint"""

    jwt.jwt_refresh_token_required()

    async with ioc.refresh_token(jwt) as interactor:
        response = await interactor(
            RefreshTokenInputDTO(
                user_id=UserId(jwt.get_jwt_subject()),
                refresh=jwt._token,
            )
        )

        return response
