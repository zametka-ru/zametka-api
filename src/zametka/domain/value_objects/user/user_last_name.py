import re

from dataclasses import dataclass

from zametka.domain.common.value_objects.base import ValueObject
from zametka.domain.exceptions.user import InvalidUserLastNameError


@dataclass(frozen=True)
class UserLastName(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if len(self.value) > 60:
            raise InvalidUserLastNameError("Фамилия пользователя слишком длинная!")
        if len(self.value) < 2:
            raise InvalidUserLastNameError("Фамилия пользователя слишком короткая!")
        if not self.value:
            raise InvalidUserLastNameError("Поле не может быть пустым!")
        if bool(re.search(r"\d", self.value)):
            raise InvalidUserLastNameError(
                "Фамилия пользователя не может содержать цифр!"
            )
