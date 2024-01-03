from abc import abstractmethod
from typing import Optional, Protocol

from zametka.access_service.application.dto import UserIdentityDTO
from zametka.access_service.domain.entities.user_identity import UserIdentity
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_identity_id import UserIdentityId


class UserIdentityRepository(Protocol):
    @abstractmethod
    async def create(self, user: UserIdentity) -> UserIdentityDTO:
        """Create"""

    @abstractmethod
    async def get(self, user_id: UserIdentityId) -> Optional[UserIdentity]:
        """Get by id"""

    @abstractmethod
    async def get_by_email(self, email: UserEmail) -> Optional[UserIdentity]:
        """Get by email"""

    @abstractmethod
    async def update(self, user_id: UserIdentityId, updated_user: UserIdentity) -> None:
        """Update"""
