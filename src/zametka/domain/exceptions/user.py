from .base import DomainError


class UserDataError(DomainError):
    pass


class UserIsNotExistsError(DomainError):
    pass


class IsNotAuthorizedError(DomainError):
    pass


class UserIsNotActiveError(DomainError):
    pass


class InvalidCredentialsError(DomainError):
    pass


class WeakPasswordError(DomainError):
    pass


class InvalidUserFirstNameError(UserDataError):
    pass


class InvalidUserLastNameError(UserDataError):
    pass


class InvalidUserEmailError(UserDataError):
    pass
