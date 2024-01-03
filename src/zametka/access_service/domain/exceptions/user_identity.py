from zametka.access_service.domain.exceptions.base import DomainError


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


class InvalidUserEmailError(DomainError):
    pass
