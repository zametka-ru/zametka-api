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

    @validator("password")
    def validate_password(cls, password: str) -> str:
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

        return password

    @root_validator
    def check_passwords_match(cls, values):
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


class AuthResponse(BaseModel):
    status: str = "ok"


class AuthFailedResponse(AuthResponse):
    status: str = "failed"
    details: str


class RegisterSuccessResponse(AuthResponse):
    pass


class RegisterFailedResponse(AuthFailedResponse):
    pass


class VerifyEmailSuccessResponse(AuthResponse):
    email: str


class VerifyEmailFailedResponse(AuthFailedResponse):
    pass


class LoginSuccessResponse(AuthResponse):
    pass


class LoginFailedResponse(AuthFailedResponse):
    pass


class RefreshSuccessResponse(AuthResponse):
    pass
