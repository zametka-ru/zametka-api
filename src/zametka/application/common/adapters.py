from abc import abstractmethod
from typing import Protocol

from zametka.domain.entities.user import User
from zametka.domain.services.email_token_service import EmailTokenService, Payload
from zametka.domain.value_objects.user.user_email import UserEmail
from zametka.domain.value_objects.user.user_hashed_password import UserHashedPassword
from zametka.domain.value_objects.email_token import EmailToken


class TokenSender(Protocol):
    """Token sender interface"""

    @abstractmethod
    def create(
        self,
        secret_key: str,
        algorithm: str,
        user: User,
        jwt: "JWTOperations",
        email_token_service: EmailTokenService,
    ) -> EmailToken:
        """Create verification token"""


class MailTokenSender(TokenSender):
    """Token sender via email interface"""

    @abstractmethod
    def send(self, token: EmailToken, subject: str, to_email: UserEmail) -> None:
        """Send token to the user via email"""


class JWTOperations(Protocol):
    """JWT Operations interface"""

    @abstractmethod
    def encode(self, payload: Payload, secret_key: str, algorithm: str) -> str:
        """Encode JWT"""

    @abstractmethod
    def decode(self, token: str, secret_key: str, algorithm: str) -> Payload:
        """Decode JWT"""


class JWT(Protocol):
    """JWT Tokens management"""

    _token: str

    @abstractmethod
    def create_access_token(self, subject: str) -> str:
        """Create access JWT"""

    @abstractmethod
    def set_access_cookies(self, token: str) -> None:
        """Set access cookies"""

    @abstractmethod
    def get_jwt_subject(self) -> str | int:
        pass


class PasswordHasher(Protocol):
    """CryptContext interface"""

    @abstractmethod
    def hash(self, plain: str) -> UserHashedPassword:
        """Hash the plain password"""

    @abstractmethod
    def verify(self, plain: str, hashed: UserHashedPassword) -> bool:
        """Compare that plain hash is equal hashed"""
