from zametka.access_service.domain.exceptions.base import DomainError


class UserDataError(DomainError):
    pass


class InvalidUserFirstNameError(UserDataError):
    pass


class InvalidUserLastNameError(UserDataError):
    pass


class UserIsNotExistsError(DomainError):
    pass


class IsNotAuthorizedError(DomainError):
    pass
