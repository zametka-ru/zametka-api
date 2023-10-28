from abc import ABC, abstractmethod

from domain.entities import RefreshToken
from domain.entities.user import User
from domain.entities import Script
from domain.value_objects.script_id import ScriptId

from domain.value_objects.user_id import UserId


class AbstractRepository(ABC):
    """Abstract implementation of SA repository"""

    def __init__(self, session) -> None:
        self.session = session


class AuthRepository(AbstractRepository):
    """User repository interface"""

    @abstractmethod
    async def create(self, user: User) -> User:
        """Create user"""

    @abstractmethod
    async def get(self, user_id: UserId) -> User:
        """Get user by id"""

    @abstractmethod
    async def get_by_email(self, email: str) -> User:
        """Get user by email"""

    @abstractmethod
    async def set_active(self, user_id: UserId) -> None:
        """Set user active"""


class ScriptRepository(AbstractRepository):
    """Script repository interface"""

    @abstractmethod
    async def create(self, script: Script) -> Script:
        """Create script"""

    @abstractmethod
    async def get(self, script_id: ScriptId) -> Script:
        """Get script by id"""

    @abstractmethod
    async def update(self, script_id: ScriptId, script: Script) -> Script:
        """Update script"""

    @abstractmethod
    async def delete(self, script_id: ScriptId) -> None:
        """Delete script"""


class RefreshTokenRepository(AbstractRepository):
    """Refresh token repository interface"""

    @abstractmethod
    async def create(self, refresh_token: RefreshToken) -> RefreshToken:
        """Create refresh token instance"""

    @abstractmethod
    async def delete(self, user_id: UserId) -> None:
        """Delete user tokens"""

    @abstractmethod
    async def exists(self, token: RefreshToken) -> bool:
        """Is token exists"""
