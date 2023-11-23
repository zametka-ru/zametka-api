from abc import abstractmethod
from typing import Protocol

from yourscript.domain.value_objects.user_id import UserId


class IdProvider(Protocol):
    @abstractmethod
    def get_current_user_id(self) -> UserId:
        raise NotImplementedError
