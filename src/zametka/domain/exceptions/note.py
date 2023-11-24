from .base import DomainError


class NoteNotExistsError(DomainError):
    pass


class NoteAccessDeniedError(DomainError):
    pass
