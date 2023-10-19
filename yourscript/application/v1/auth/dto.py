import dataclasses


@dataclasses.dataclass
class VerificationInputDTO:
    token: str


@dataclasses.dataclass
class LoginInputDTO:
    user_email: str
    user_password: str
