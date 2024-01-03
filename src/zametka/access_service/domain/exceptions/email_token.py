from zametka.access_service.domain.exceptions.base import DomainError


class EmailTokenAlreadyUsedError(DomainError):
    pass


class CorruptedEmailTokenError(DomainError):
    pass
