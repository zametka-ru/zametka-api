from abc import ABC, abstractmethod


class TokenSenderInterface(ABC):
    """Token sender interface"""

    @abstractmethod
    def send(self, token: str):
        """Send token to the user"""


class MailTokenSenderInterface(ABC):
    """Token sender via email interface"""

    @abstractmethod
    def send(self, token: str, subject: str, to_email: str):
        """Send token to the user via email"""


class JWTOpsInterface(ABC):
    """JWT Operations interface"""

    @abstractmethod
    def encode(self, payload: dict, secret_key: str, algorithm: str) -> str:
        """Encode JWT"""

    @abstractmethod
    def decode(self, token: str, secret_key: str, algorithm: str) -> dict:
        """Decode JWT"""
