from .base import DomainError


class UserIsNotExists(DomainError):
    pass


class UserIsNotActive(DomainError):
    pass


class InvalidCredentials(DomainError):
    pass


class WeakPasswordError(DomainError):
    pass
