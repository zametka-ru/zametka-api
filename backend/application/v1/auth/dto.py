import dataclasses

from fastapi_jwt_auth import AuthJWT
from fastapi_mail import FastMail
from passlib.context import CryptContext
from starlette.background import BackgroundTasks

from core.settings import AuthSettings
from presentation.v1.schemas.auth import UserLoginSchema

from repository import UnitOfWork


@dataclasses.dataclass
class RegisterInputDTO:
    user_data: dict
    background_tasks: BackgroundTasks
    pwd_context: CryptContext
    mail_context: FastMail
    auth_settings: AuthSettings
    uow: UnitOfWork


@dataclasses.dataclass
class VerificationInputDTO:
    token: str
    auth_settings: AuthSettings
    uow: UnitOfWork


@dataclasses.dataclass
class LoginInputDTO:
    user_login: UserLoginSchema
    Authorize: AuthJWT
    pwd_context: CryptContext
