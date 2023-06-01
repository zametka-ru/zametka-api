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


class UnitOfWorkDependency(ABC):
    """
    It's a dependency for UnitOfWork instance
    """
