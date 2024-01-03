from dataclasses import dataclass
from uuid import UUID

from zametka.access_service.domain.common.value_objects.base import ValueObject


@dataclass(frozen=True)
class UserIdentityId(ValueObject[UUID]):
    value: UUID
