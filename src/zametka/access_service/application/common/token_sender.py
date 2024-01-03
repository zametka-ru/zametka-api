from abc import abstractmethod

from typing import Protocol

from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.email_token import EmailToken


class TokenSender(Protocol):
    """Token sender interface"""


class MailTokenSender(TokenSender):
    """Token sender via email interface"""

    @abstractmethod
    def send(self, token: EmailToken, subject: str, to_email: UserEmail) -> None:
        """Send token to the user via email"""
