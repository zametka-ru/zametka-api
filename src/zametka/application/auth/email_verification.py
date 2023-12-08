from dataclasses import dataclass
from datetime import datetime

from typing import Optional

from zametka.application.common.adapters import JWTOperations
from zametka.application.common.interactor import Interactor
from zametka.application.common.repository import AuthRepository
from zametka.application.common.uow import UoW
from zametka.domain.entities.user import DBUser

from zametka.domain.exceptions.email_token import (
    CorruptedEmailTokenError,
)
from zametka.domain.services.email_token_service import EmailTokenService
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
        repository: AuthRepository,
        uow: UoW,
        jwt_ops: JWTOperations,
        secret_key: str,
        algorithm: str,
        email_token_service: EmailTokenService,
    ):
        self.uow = uow
        self.jwt_ops = jwt_ops
        self.repository = repository
        self._secret_key = secret_key
        self._algorithm = algorithm
        self.email_token_service = email_token_service

    async def __call__(
        self, data: EmailVerificationInputDTO
    ) -> EmailVerificationOutputDTO:
        secret_key: str = self._secret_key
        algorithm: str = self._algorithm

        payload = self.jwt_ops.decode(data.token, secret_key, algorithm)

        user_email: Optional[str | bool | datetime] = payload.get("user_email")

        if not user_email or not isinstance(user_email, str):
            raise CorruptedEmailTokenError()

        user: Optional[DBUser] = await self.repository.get_by_email(
            UserEmail(user_email)
        )

        if not user:
            raise CorruptedEmailTokenError()

        decoded_user: DBUser = self.email_token_service.check_payload(user, payload)

        await self.repository.set_active(decoded_user.user_id)
        await self.uow.commit()

        return EmailVerificationOutputDTO(email=decoded_user.email.to_raw())
