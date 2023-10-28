from .base import DomainError


class ScriptNotExists(DomainError):
    pass


class ScriptAccessDenied(DomainError):
    pass
