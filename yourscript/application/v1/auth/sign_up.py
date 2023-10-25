from dataclasses import dataclass

from application.common.adapters import (
    JWTOperations,
    AuthSettings,
    MailTokenSender,
    PasswordHasher,
    HashedPassword,
)
from application.common.interactor import Interactor
from application.common.repository import AuthRepository
from application.common.uow import UoW

from domain.v1.services.user_service import UserService


@dataclass
class SignUpOutputDTO:
    pass


@dataclass
class SignUpInputDTO:
    user_email: str
    user_password: str
    user_first_name: str
    user_last_name: str


class SignUp(Interactor[SignUpInputDTO, SignUpOutputDTO]):
    def __init__(
        self,
        repository: AuthRepository,
        pwd_context: PasswordHasher,
        token_sender: MailTokenSender,
        auth_settings: AuthSettings,
        uow: UoW,
        jwt: JWTOperations,
        service: UserService,
    ):
        self.uow = uow
        self.jwt = jwt
        self.service = service
        self.auth_settings = auth_settings
        self.pwd_context = pwd_context
        self.token_sender = token_sender
        self.repository = repository

    async def __call__(self, data: SignUpInputDTO) -> SignUpOutputDTO:
        user_password: str = data.user_password

        self.service.check_password(user_password)

        user_password: HashedPassword = self.pwd_context.hash(user_password)

        user = self.service.create(
            email=data.user_email,
            password=user_password,
            first_name=data.user_first_name,
            last_name=data.user_last_name,
        )

        await self.repository.create(user)

        await self.uow.commit()

        secret_key: str = self.auth_settings.secret_key
        algorithm: str = self.auth_settings.algorithm

        token: str = self.token_sender.create(secret_key, algorithm, user, self.jwt)

        self.token_sender.send(
            token, subject="Завершите регистрацию в yourscript.", to_email=user.email
        )

        return SignUpOutputDTO()
