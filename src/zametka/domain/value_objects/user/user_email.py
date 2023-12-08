from dataclasses import dataclass

from zametka.domain.common.value_objects.base import ValueObject
from zametka.domain.exceptions.user import InvalidUserEmailError


@dataclass(frozen=True)
class UserEmail(ValueObject[str]):
    value: str

    def validate(self) -> None:
        if len(self.value) > 100:
            raise InvalidUserEmailError("Слишком длинный e-mail!")
