from dataclasses import dataclass


@dataclass
class AuthFailedResponse:
    details: str
    code: int

@dataclass
class RegisterSuccessResponse:
    pass

@dataclass
class RegisterFailedResponse(AuthFailedResponse):
    pass

@dataclass
class VerifyEmailSuccessResponse:
    email: str

@dataclass
class VerifyEmailFailedResponse(AuthFailedResponse):
    pass

@dataclass
class LoginSuccessResponse:
    pass

@dataclass
class LoginFailedResponse(AuthFailedResponse):
    pass

@dataclass
class RefreshSuccessResponse:
    pass
