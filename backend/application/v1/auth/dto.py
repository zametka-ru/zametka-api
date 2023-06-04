import dataclasses

from presentation.v1.schemas.auth import UserLoginSchema


@dataclasses.dataclass
class RegisterInputDTO:
    user_email: str
    user_password: str
    user_first_name: str
    user_last_name: str


@dataclasses.dataclass
class VerificationInputDTO:
    token: str


@dataclasses.dataclass
class LoginInputDTO:
    user_email: str
    user_password: str
