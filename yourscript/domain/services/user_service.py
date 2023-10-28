import datetime

from domain.entities.user import User


class UserService:
    def check_password(self, password: str) -> None:
        """Validate password"""

        error_messages = {
            "Password must contain an uppercase letter.": lambda s: any(
                x.isupper() for x in s
            ),
            "Password must contain a lowercase letter.": lambda s: any(
                x.islower() for x in s
            ),
            "Password must contain a digit.": lambda s: any(x.isdigit() for x in s),
            "Password cannot contain white spaces.": lambda s: not any(
                x.isspace() for x in s
            ),
        }

        for message, password_validator in error_messages.items():
            if not password_validator(password):
                raise ValueError(message)

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
