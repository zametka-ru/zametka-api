from dataclasses import dataclass

from zametka.access_service.domain.common.value_objects.base import ValueObject


@dataclass(frozen=True)
class EmailToken(ValueObject[str]):
    value: str
