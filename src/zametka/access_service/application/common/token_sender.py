from abc import abstractmethod

from typing import Protocol

from zametka.access_service.domain.entities.user_identity import UserIdentity
from zametka.access_service.domain.entities.confirmation_token import (
    IdentityConfirmationToken,
)


class TokenSender(Protocol):
    """Token sender interface"""

    @abstractmethod
    async def send(
        self, confirmation_token: IdentityConfirmationToken, user: UserIdentity
    ) -> None:
        raise NotImplementedError
