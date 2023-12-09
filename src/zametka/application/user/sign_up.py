from dataclasses import dataclass

from zametka.application.user.dto import UserDTO
from zametka.application.common.password_hasher import (
    PasswordHasher,
)
from zametka.application.common.token_sender import MailTokenSender
from zametka.application.common.interactor import Interactor
from zametka.application.common.repository import UserRepository
from zametka.application.common.uow import UoW
from zametka.domain.services.email_token_service import EmailTokenService
from zametka.domain.services.user_service import UserService
from zametka.domain.value_objects.email_token import EmailToken
from zametka.domain.value_objects.user.user_email import UserEmail
from zametka.domain.value_objects.user.user_first_name import UserFirstName
from zametka.domain.value_objects.user.user_hashed_password import UserHashedPassword
from zametka.domain.value_objects.user.user_last_name import UserLastName
from zametka.domain.value_objects.user.user_raw_password import UserRawPassword


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
        user_repository: UserRepository,
        pwd_context: PasswordHasher,
        token_sender: MailTokenSender,
        uow: UoW,
        service: UserService,
        email_token_service: EmailTokenService,
        secret_key: str,
        algorithm: str,
    ):
        self.uow = uow
        self.service = service
        self.pwd_context = pwd_context
        self.token_sender = token_sender
        self.user_repository = user_repository
        self._secret_key = secret_key
        self._algorithm = algorithm
        self.email_token_service = email_token_service

    async def __call__(self, data: SignUpInputDTO) -> SignUpOutputDTO:
        email = UserEmail(data.user_email)
        raw_password = UserRawPassword(data.user_password)
        hashed_password: UserHashedPassword = self.pwd_context.hash(raw_password)
        first_name = UserFirstName(data.user_first_name)
        last_name = UserLastName(data.user_last_name)

        user = self.service.create(
            email=email,
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name,
        )

        user_dto = await self.user_repository.create(user)

        await self.uow.commit()

        secret_key: str = self._secret_key
        algorithm: str = self._algorithm

        token: EmailToken = self.email_token_service.encode_token(
            user, secret_key, algorithm
        )

        self.token_sender.send(
            token, subject="Завершите регистрацию в yourscript.", to_email=user.email
        )

        return SignUpOutputDTO(user=user_dto)
