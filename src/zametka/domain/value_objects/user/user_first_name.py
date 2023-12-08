import re

from dataclasses import dataclass

from zametka.domain.common.value_objects.base import ValueObject
from zametka.domain.exceptions.user import InvalidUserFirstNameError


@dataclass(frozen=True)
class UserFirstName(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if len(self.value) > 40:
            raise InvalidUserFirstNameError("Имя пользователя слишком длинное!")
        if len(self.value) < 2:
            raise InvalidUserFirstNameError("Имя пользователя слишком короткое!")
        if not self.value:
            raise InvalidUserFirstNameError("Поле не может быть пустым!")
        if bool(re.search(r"\d", self.value)):
            raise InvalidUserFirstNameError("Имя пользователя не может содержать цифр!")
