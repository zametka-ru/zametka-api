from abc import abstractmethod

from typing import Protocol, NewType

from domain.v1.entities.user import User

HashedPassword = NewType("HashedPassword", str)
Token = NewType("Token", str)


class TokenSender(Protocol):
    """Token sender interface"""

    @abstractmethod
    def create(self, secret_key: str, algorithm: str, user: User, jwt: 'JWT') -> Token:
        """Create verification token"""


class MailTokenSender(TokenSender):
    """Token sender via email interface"""

    @abstractmethod
    def send(self, token: str, subject: str, to_email: str):
        """Send token to the user via email"""


class JWT(Protocol):
    """JWT Operations interface"""

    @abstractmethod
    def encode(self, payload: dict, secret_key: str, algorithm: str) -> str:
        """Encode JWT"""

    @abstractmethod
    def decode(self, token: str, secret_key: str, algorithm: str) -> dict:
        """Decode JWT"""


class PasswordHasher(Protocol):
    """CryptContext interface"""

    @abstractmethod
    def hash(self, plain: str) -> HashedPassword:
        """Hash the plain password"""


class AuthSettings(Protocol):
    """Auth settings interface"""

    secret_key: str
    algorithm: str
