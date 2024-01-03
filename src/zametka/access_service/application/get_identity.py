from typing import Optional

from zametka.access_service.application.dto import UserIdentityDTO
from zametka.access_service.application.common.id_provider import IdProvider
from zametka.access_service.application.common.interactor import Interactor
from zametka.access_service.application.common.repository import UserIdentityRepository
from zametka.access_service.domain.entities.user_identity import UserIdentity
from zametka.access_service.domain.exceptions.user_identity import IsNotAuthorizedError
from zametka.access_service.domain.services.user_identity_service import (
    UserIdentityService,
)


class GetIdentity(Interactor[None, UserIdentityDTO]):
    def __init__(
        self,
        user_repository: UserIdentityRepository,
        user_service: UserIdentityService,
        id_provider: IdProvider,
    ):
        self.user_repository = user_repository
        self.user_service = user_service
        self.id_provider = id_provider

    async def _get_current_user(self) -> UserIdentity:
        user_id = self.id_provider.get_identity_id()

        user: Optional[UserIdentity] = await self.user_repository.get(user_id)

        if not user:
            raise IsNotAuthorizedError()

        self.user_service.ensure_can_access(user)

        return user

    async def __call__(self, data=None) -> UserIdentityDTO:  # type:ignore
        user = await self._get_current_user()

        return UserIdentityDTO(
            identity_id=user.identity_id.to_raw(),
        )
