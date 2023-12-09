from email_validator import EmailNotValidError, validate_email
from pydantic import BaseModel, root_validator, validator

from zametka.domain.exceptions.user import InvalidUserEmailError


def email_validator(email: str) -> str:
    try:
        email_info = validate_email(email, check_deliverability=False)
    except EmailNotValidError:
        raise InvalidUserEmailError("Неправильный e-mail!")

    email = email_info.original_email

    return email


# noinspection PyMethodParameters
class UserRegisterSchema(BaseModel):
    """User register schema"""

    email: str
    password: str
    password2: str
    first_name: str
    last_name: str
    is_superuser: bool = False
    is_active: bool = False

    @validator("email")
    def validate_email(cls, email: str) -> str:
        """Validate email"""

        return email_validator(email)

    @root_validator
    def pop_superuser(cls, values: dict[str, bool]) -> dict[str, bool]:
        values.pop(
            "is_superuser", False
        )  # superuser field must be set manually by admin

        return values

    @root_validator
    def check_passwords_match(cls, values: dict[str, bool]) -> dict[str, bool]:
        pw1, pw2 = values.get("password"), values.get("password2")

        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("Пароли не совпадают")

        return values


class UserLoginSchema(BaseModel):
    """User login schema"""

    email: str
    password: str

    # noinspection PyMethodParameters
    @validator("email")
    def validate_email(cls, email: str) -> str:
        """Validate email"""

        return email_validator(email)
