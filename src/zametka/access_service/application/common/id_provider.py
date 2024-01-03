from abc import abstractmethod
from typing import Protocol

from zametka.access_service.domain.value_objects.user_identity_id import UserIdentityId


class IdProvider(Protocol):
    @abstractmethod
    def get_identity_id(self) -> UserIdentityId:
        raise NotImplementedError
