import dataclasses

from fastapi_mail import FastMail
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

from core.settings import AuthSettings


@dataclasses.dataclass
class RegisterInputDTO:
    user_data: dict
    background_tasks: BackgroundTasks
    pwd_context: CryptContext
    session: Session
    mail_context: FastMail
    auth_settings: AuthSettings


@dataclasses.dataclass
class VerificationInputDTO:
    token: str
    session: Session
    auth_settings: AuthSettings
