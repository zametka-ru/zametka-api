from abc import ABC, abstractmethod


class TokenSenderInterface(ABC):
    @abstractmethod
    def send(self, *args, **kwargs):
        """Send token to the user"""
