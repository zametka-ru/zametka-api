from dataclasses import dataclass
from typing import Union
from uuid import UUID

from zametka.access_service.domain.common.value_objects.base import ValueObject


@dataclass(frozen=True)
class UserIdentityId(ValueObject[UUID]):
    value: UUID

    def __eq__(self, other: Union["UserIdentityId", object]) -> bool:
        if not isinstance(other, UserIdentityId):
            return self.to_raw() == other
        return self.to_raw() == other.to_raw()
