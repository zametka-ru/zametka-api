from dataclasses import dataclass
from datetime import datetime

from typing import Optional

from zametka.application.common.interactor import Interactor
from zametka.application.common.repository import UserRepository
from zametka.application.common.uow import UoW
from zametka.domain.entities.user import DBUser

from zametka.domain.exceptions.email_token import (
    CorruptedEmailTokenError,
)
from zametka.domain.services.email_token_service import EmailTokenService
from zametka.domain.value_objects.email_token import EmailToken
from zametka.domain.value_objects.user.user_email import UserEmail


@dataclass(frozen=True)
class EmailVerificationInputDTO:
    token: str


@dataclass(frozen=True)
class EmailVerificationOutputDTO:
    email: Optional[str]


class EmailVerification(
    Interactor[EmailVerificationInputDTO, EmailVerificationOutputDTO]
):
    def __init__(
        self,
        user_repository: UserRepository,
        uow: UoW,
        secret_key: str,
        algorithm: str,
        email_token_service: EmailTokenService,
    ):
        self.uow = uow
        self.user_repository = user_repository
        self._secret_key = secret_key
        self._algorithm = algorithm
        self.email_token_service = email_token_service

    async def __call__(
        self, data: EmailVerificationInputDTO
    ) -> EmailVerificationOutputDTO:
        secret_key: str = self._secret_key
        algorithm: str = self._algorithm

        payload = self.email_token_service.decode_token(
            EmailToken(data.token), secret_key, algorithm
        )

        user_email: Optional[str | bool | datetime] = payload.get("user_email")

        if not user_email or not isinstance(user_email, str):
            raise CorruptedEmailTokenError()

        user: Optional[DBUser] = await self.user_repository.get_by_email(
            UserEmail(user_email)
        )

        if not user:
            raise CorruptedEmailTokenError()

        decoded_user: DBUser = self.email_token_service.activate_user(user, payload)

        await self.user_repository.update(decoded_user.user_id, decoded_user)
        await self.uow.commit()

        return EmailVerificationOutputDTO(email=decoded_user.email.to_raw())
