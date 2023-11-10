from .base import DomainError


class TokenAlreadyUsedError(DomainError):
    pass


class CorruptedTokenError(DomainError):
    pass
