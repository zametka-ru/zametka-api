import datetime
import re

from zametka.domain.entities.user import DBUser, User
from zametka.domain.exceptions.user import UserIsNotActiveError, WeakPasswordError


class UserService:
    def check_password(self, password: str) -> None:
        """Validate password"""

        special_symbols_regex = re.compile("[@_!#$%^&*()<>?/}{~:]")

        error_messages = {
            "Пароль должен содержать заглавную букву.": lambda s: any(
                x.isupper() for x in s
            ),
            "Пароль не должен состоять только из заглавных букв.": lambda s: any(
                x.islower() for x in s
            ),
            "Пароль должен содержать число.": lambda s: any(x.isdigit() for x in s),
            "Пароль не должен содержать пробелы.": lambda s: not any(
                x.isspace() for x in s
            ),
            "Пароль должен содержать в себе специальный символ (@, #, $, %)": lambda s: re.search(
                special_symbols_regex, s
            )
            is not None,
        }

        for message, password_validator in error_messages.items():
            if not password_validator(password):
                raise WeakPasswordError(message)

    def create(
        self, email: str, password: str, first_name: str, last_name: str
    ) -> User:
        self.check_password(password)

        return User(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            joined_at=datetime.datetime.now(),
        )

    def ensure_can_login(self, user: DBUser) -> None:
        if not user.is_active:
            raise UserIsNotActiveError
