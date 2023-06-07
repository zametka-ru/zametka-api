from dataclasses import dataclass


@dataclass
class RegisterSuccessResponse:
    pass


@dataclass
class VerifyEmailSuccessResponse:
    user_id: int


@dataclass
class LoginSuccessResponse:
    pass


@dataclass
class RefreshSuccessResponse:
    pass
