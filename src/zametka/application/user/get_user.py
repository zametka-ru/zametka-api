from dataclasses import dataclass
from typing import Optional

from zametka.application.user.dto import DBUserDTO
from zametka.application.common.id_provider import IdProvider
from zametka.application.common.interactor import Interactor
from zametka.application.common.repository import UserRepository
from zametka.domain.entities.user import DBUser
from zametka.domain.exceptions.user import IsNotAuthorizedError
from zametka.domain.services.user_service import UserService


@dataclass(frozen=True)
class GetUserInputDTO:
    pass


class GetUser(Interactor[GetUserInputDTO, DBUserDTO]):
    def __init__(
        self,
        user_repository: UserRepository,
        user_service: UserService,
        id_provider: IdProvider,
    ):
        self.user_repository = user_repository
        self.user_service = user_service
        self.id_provider = id_provider

    async def _get_current_user(self) -> DBUser:
        """Get current userT"""

        user_id = self.id_provider.get_current_user_id()

        user: Optional[DBUser] = await self.user_repository.get(user_id)

        if not user:
            raise IsNotAuthorizedError()

        self.user_service.ensure_can_access(user)

        return user

    async def __call__(self, data: GetUserInputDTO) -> DBUserDTO:
        user = await self._get_current_user()

        return DBUserDTO(
            user_id=user.user_id.to_raw(),
            email=user.email.to_raw(),
            first_name=user.first_name.to_raw(),
            last_name=user.last_name.to_raw(),
            joined_at=user.joined_at.read(),
        )
