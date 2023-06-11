from abc import ABC


class MailDependency(ABC):
    """
    It's a dependency for FastMail instance
    """


class AuthSettingsDependency(ABC):
    """
    It's a dependency for AuthSettings instance
    """


class AuthRepositoryDependency(ABC):
    """
    It's a dependency for AuthRepository instance
    """


class ScriptRepositoryDependency(ABC):
    """
    It's a dependency for ScriptRepository instance
    """


class UnitOfWorkDependency(ABC):
    """
    It's a dependency for UnitOfWork instance
    """


class CryptContextDependency(ABC):
    """
    It's a dependency for CryptContext instance
    """


class AuthJWTDependency(ABC):
    """
    It's a dependency for AuthJWT instance
    """


class SessionDependency(ABC):
    """
    It's a dependency for Session instance
    """


class JinjaDependency(ABC):
    """It's a dependency for jinja2 environment"""
