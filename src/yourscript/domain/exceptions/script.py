from .base import DomainError


class ScriptNotExistsError(DomainError):
    pass


class ScriptAccessDeniedError(DomainError):
    pass
