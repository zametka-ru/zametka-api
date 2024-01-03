from dataclasses import dataclass

from zametka.access_service.domain.common.value_objects.base import ValueObject


@dataclass(frozen=True)
class UserHashedPassword(ValueObject[str]):
    value: str
