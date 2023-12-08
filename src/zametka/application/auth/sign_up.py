from dataclasses import dataclass

from zametka.application.auth.dto import UserDTO
from zametka.application.common.adapters import (
    JWTOperations,
    MailTokenSender,
    PasswordHasher,
)
from zametka.application.common.interactor import Interactor
from zametka.application.common.repository import AuthRepository
from zametka.application.common.uow import UoW
from zametka.domain.services.email_token_service import EmailTokenService
from zametka.domain.services.user_service import UserService
from zametka.domain.value_objects.email_token import EmailToken
from zametka.domain.value_objects.user.user_email import UserEmail
from zametka.domain.value_objects.user.user_first_name import UserFirstName
from zametka.domain.value_objects.user.user_hashed_password import UserHashedPassword
from zametka.domain.value_objects.user.user_last_name import UserLastName


@dataclass(frozen=True)
class SignUpOutputDTO:
    user: UserDTO


@dataclass(frozen=True)
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
        uow: UoW,
        jwt_ops: JWTOperations,
        service: UserService,
        email_token_service: EmailTokenService,
        secret_key: str,
        algorithm: str,
    ):
        self.uow = uow
        self.jwt_ops = jwt_ops
        self.service = service
        self.pwd_context = pwd_context
        self.token_sender = token_sender
        self.repository = repository
        self._secret_key = secret_key
        self._algorithm = algorithm
        self.email_token_service = email_token_service

    async def __call__(self, data: SignUpInputDTO) -> SignUpOutputDTO:
        self.service.check_password(data.user_password)

        email = UserEmail(data.user_email)
        hashed_password: UserHashedPassword = self.pwd_context.hash(data.user_password)
        first_name = UserFirstName(data.user_first_name)
        last_name = UserLastName(data.user_last_name)

        user = self.service.create(
            email=email,
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name,
        )

        user_dto = await self.repository.create(user)

        await self.uow.commit()

        secret_key: str = self._secret_key
        algorithm: str = self._algorithm

        token: EmailToken = self.token_sender.create(
            secret_key, algorithm, user, self.jwt_ops, self.email_token_service
        )

        self.token_sender.send(
            token, subject="Завершите регистрацию в yourscript.", to_email=user.email
        )

        return SignUpOutputDTO(user=user_dto)
