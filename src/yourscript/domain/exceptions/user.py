from .base import DomainError


class UserIsNotExistsError(DomainError):
    pass


class UserIsNotActiveError(DomainError):
    pass


class InvalidCredentialsError(DomainError):
    pass


class WeakPasswordError(DomainError):
    pass
