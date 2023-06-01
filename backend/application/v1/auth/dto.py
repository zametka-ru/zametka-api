import dataclasses

from fastapi_mail import FastMail
from passlib.context import CryptContext
from starlette.background import BackgroundTasks

from core.settings import AuthSettings

from repository import AuthRepository


@dataclasses.dataclass
class RegisterInputDTO:
    user_data: dict
    background_tasks: BackgroundTasks
    pwd_context: CryptContext
    mail_context: FastMail
    repository: AuthRepository
    auth_settings: AuthSettings


@dataclasses.dataclass
class VerificationInputDTO:
    token: str
    auth_settings: AuthSettings
    repository: AuthRepository
