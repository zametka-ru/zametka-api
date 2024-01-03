from dataclasses import dataclass

from typing import Optional

from zametka.access_service.application.common.interactor import Interactor
from zametka.access_service.application.common.repository import UserIdentityRepository
from zametka.access_service.application.common.uow import UoW
from zametka.access_service.domain.entities.user_identity import UserIdentity

from zametka.access_service.domain.exceptions.email_token import (
    CorruptedEmailTokenError,
)
from zametka.access_service.domain.services.email_token_service import (
    EmailTokenService,
    PayloadSub,
)
from zametka.access_service.domain.value_objects.email_token import EmailToken
from zametka.access_service.domain.value_objects.user_email import UserEmail


@dataclass(frozen=True)
class TokenInputDTO:
    token: str


class VerifyEmail(Interactor[TokenInputDTO, None]):
    def __init__(
        self,
        user_repository: UserIdentityRepository,
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

    async def __call__(self, data: TokenInputDTO) -> None:
        secret_key: str = self._secret_key
        algorithm: str = self._algorithm

        payload_sub: PayloadSub = self.email_token_service.decode_token(
            EmailToken(data.token), secret_key, algorithm
        )

        user_email: Optional[str | bool] = payload_sub.get("email")

        if not user_email or not isinstance(user_email, str):
            raise CorruptedEmailTokenError()

        user: Optional[UserIdentity] = await self.user_repository.get_by_email(
            UserEmail(user_email)
        )

        if not user:
            raise CorruptedEmailTokenError()

        decoded_user: UserIdentity = self.email_token_service.activate_user(
            user, payload_sub
        )

        await self.user_repository.update(decoded_user.identity_id, decoded_user)
        await self.uow.commit()

        return None
