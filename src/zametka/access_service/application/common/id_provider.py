from abc import abstractmethod
from typing import Protocol

from zametka.access_service.domain.entities.user_identity import UserIdentity
from zametka.access_service.domain.value_objects.user_identity_id import UserIdentityId


class IdProvider(Protocol):
    @abstractmethod
    def get_identity_id(self) -> UserIdentityId:
        raise NotImplementedError


class UserProvider(IdProvider):
    @abstractmethod
    async def get_user(self) -> UserIdentity:
        raise NotImplementedError
