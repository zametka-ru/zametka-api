from abc import abstractmethod
from typing import Protocol

from zametka.notes.domain.value_objects.user.user_identity_id import UserIdentityId


class IdProvider(Protocol):
    @abstractmethod
    async def get_identity_id(self) -> UserIdentityId:
        raise NotImplementedError
