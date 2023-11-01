import re

from pydantic import BaseModel, Field, validator, root_validator

from email_validator import validate_email


# noinspection PyMethodParameters
class UserRegisterSchema(BaseModel):
    """User register schema"""

    email: str = Field(max_length=60)
    password: str = Field(max_length=30, min_length=6)
    password2: str = Field(max_length=30, min_length=6)
    first_name: str = Field(max_length=40)
    last_name: str = Field(max_length=60)
    is_superuser: bool = False
    is_active: bool = False

    @validator("email")
    def validate_email(cls, email: str) -> str:
        """Validate email"""

        email_info = validate_email(email, check_deliverability=False)

        email = email_info.original_email

        return email

    @root_validator
    def validate_names(cls, values: dict):
        first_name = values.get("first_name")
        last_name = values.get("last_name")

        if bool(re.search(r"\d", first_name)) or bool(re.search(r"\d", last_name)):
            raise ValueError("В имени и фамилии не может быть цифр.")

        return values

    @root_validator
    def pop_superuser(cls, values: dict):
        values.pop(
            "is_superuser", False
        )  # superuser field must be set manually by admin

        return values

    @root_validator
    def check_passwords_match(cls, values: dict):
        pw1, pw2 = values.get("password"), values.get("password2")

        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("Passwords do not match.")

        return values


class UserLoginSchema(BaseModel):
    """User login schema"""

    email: str = Field(max_length=60)
    password: str = Field(max_length=30, min_length=6)

    # noinspection PyMethodParameters
    @validator("email")
    def validate_email(cls, email: str) -> str:
        """Validate email"""

        email_info = validate_email(email, check_deliverability=False)

        email = email_info.original_email

        return email
