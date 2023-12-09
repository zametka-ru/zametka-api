from abc import abstractmethod
from typing import Protocol

from zametka.domain.value_objects.user.user_hashed_password import UserHashedPassword
from zametka.domain.value_objects.user.user_raw_password import UserRawPassword


class PasswordHasher(Protocol):
    """CryptContext interface"""

    @abstractmethod
    def hash(self, plain: UserRawPassword) -> UserHashedPassword:
        """Hash the plain password"""

    @abstractmethod
    def verify(self, plain: UserRawPassword, hashed: UserHashedPassword) -> bool:
        """Compare that plain hash is equal hashed"""
