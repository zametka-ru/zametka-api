from abc import abstractmethod
from typing import Protocol

from zametka.domain.value_objects.user.user_id import UserId


class IdProvider(Protocol):
    @abstractmethod
    def get_current_user_id(self) -> UserId:
        raise NotImplementedError