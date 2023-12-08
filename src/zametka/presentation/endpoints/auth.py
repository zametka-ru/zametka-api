from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi_another_jwt_auth import AuthJWT

from zametka.application.auth.dto import DBUserDTO
from zametka.application.auth.email_verification import (
    EmailVerificationInputDTO,
    EmailVerificationOutputDTO,
)
from zametka.application.auth.get_user import GetUserInputDTO

from zametka.application.auth.sign_in import SignInInputDTO, SignInOutputDTO
from zametka.application.auth.sign_up import SignUpInputDTO, SignUpOutputDTO
from zametka.presentation.interactor_factory import InteractorFactory
from zametka.presentation.schemas.auth import UserLoginSchema, UserRegisterSchema

router = APIRouter(
    prefix="/v1/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/sign-up")
async def sign_up(
    user_data: UserRegisterSchema,
    background_tasks: BackgroundTasks,
    ioc: InteractorFactory = Depends(),
) -> SignUpOutputDTO:
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


@router.post("/sign-in")
async def sign_in(
    auth_data: UserLoginSchema,
    jwt_auth: AuthJWT = Depends(),
    ioc: InteractorFactory = Depends(),
) -> SignInOutputDTO:
    """Login endpoint"""

    async with ioc.sign_in() as interactor:
        response = await interactor(
            SignInInputDTO(email=auth_data.email, password=auth_data.password)
        )

    subject = response.user_id

    access = jwt_auth.create_access_token(subject=subject)

    jwt_auth.set_access_cookies(access)

    return response


@router.get("/whoami")
async def get_user(
    jwt_auth: AuthJWT = Depends(),
    ioc: InteractorFactory = Depends(),
) -> DBUserDTO:
    """Get user endpoint"""

    jwt_auth.jwt_required()

    async with ioc.get_user(jwt=jwt_auth) as interactor:
        response = await interactor(GetUserInputDTO())

    return response


@router.get("/verify/{token}")
async def email_verification(
    token: str, ioc: InteractorFactory = Depends()
) -> EmailVerificationOutputDTO:
    """Email verification endpoint"""

    async with ioc.email_verification() as interactor:
        response = await interactor(
            EmailVerificationInputDTO(
                token=token,
            )
        )

        return response
