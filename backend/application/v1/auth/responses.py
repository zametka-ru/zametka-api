from dataclasses import dataclass


@dataclass
class RegisterSuccessResponse:
    pass


@dataclass
class VerifyEmailSuccessResponse:
    email: str


@dataclass
class LoginSuccessResponse:
    pass


@dataclass
class RefreshSuccessResponse:
    pass
