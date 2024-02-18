from typing import Optional

from zametka.access_service.application.common.repository import UserIdentityRepository
from zametka.access_service.application.dto import UserIdentityDTO
from zametka.access_service.domain.entities.user_identity import UserIdentity
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_identity_id import UserIdentityId


class FakeUserIdentityRepository(UserIdentityRepository):
    def __init__(self, user: UserIdentity):
        self.user = user
        self.created = False
        self.updated = False
        self.deleted = False

    async def create(self, user: UserIdentity) -> UserIdentityDTO:
        self.created = True
        return UserIdentityDTO(
            identity_id=self.user.identity_id.to_raw(),
        )

    async def get(self, user_id: UserIdentityId) -> Optional[UserIdentity]:
        if not self.user.identity_id == user_id:
            return None

        return self.user

    async def get_by_email(self, email: UserEmail) -> Optional[UserIdentity]:
        if not self.user.email == email:
            return None

        return self.user

    async def update(self, user_id: UserIdentityId, updated_user: UserIdentity) -> None:
        self.updated = True

        self.user.is_active = updated_user.is_active
        self.user.email = updated_user.email
        self.user.hashed_password = updated_user.hashed_password
        self.user.identity_id = updated_user.identity_id

    async def delete(self, user_id: UserIdentityId) -> None:
        self.deleted = True
