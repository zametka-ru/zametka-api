from .base import DomainError


class EmailTokenAlreadyUsedError(DomainError):
    pass


class CorruptedEmailTokenError(DomainError):
    pass
