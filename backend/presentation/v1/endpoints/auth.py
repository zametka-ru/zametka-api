import jwt
from fastapi import APIRouter, Depends

from fastapi_jwt_auth import AuthJWT
from fastapi_mail import FastMail
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

from core.settings import load_authjwt_settings, AuthJWTSettings, AuthSettings
from core.dependencies import MailDependency, AuthSettingsDependency

from application.v1.auth import register_user, user_verify_email

from ..schemas.auth import (
    UserRegisterSchema,
    RegisterSuccessResponse,
    RegisterFailedResponse,
    VerifyEmailSuccessResponse,
    VerifyEmailFailedResponse,
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
    session: Session = Depends(),
    mail_context: MailDependency = Depends(),
):
    mail_context: FastMail  # type:ignore
    auth_settings: AuthSettings  # type:ignore

    register_data_dict: dict = register_data.dict()

    response = await register_user(
        register_data_dict,
        background_tasks,
        pwd_context,
        session,
        mail_context,
        auth_settings,
    )

    return response


@router.get("/verify/{token}")
async def verify_email(
    token: str,
    auth_settings: AuthSettingsDependency = Depends(),
    session: Session = Depends(),
):
    auth_settings: AuthSettings  # type:ignore

    return await user_verify_email(token, auth_settings, session)


@router.post("/refresh")
async def refresh(Authorize: AuthJWT = Depends()):
    """Refresh JWT"""

    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}
