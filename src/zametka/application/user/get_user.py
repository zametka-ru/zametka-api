from dataclasses import dataclass
from typing import Optional

from zametka.application.user.dto import DBUserDTO
from zametka.application.common.id_provider import IdProvider
from zametka.application.common.interactor import Interactor
from zametka.application.common.repository import UserRepository
from zametka.domain.entities.user import DBUser
from zametka.domain.exceptions.user import IsNotAuthorizedError


@dataclass(frozen=True)
class GetUserInputDTO:
    pass


class GetUser(Interactor[GetUserInputDTO, DBUserDTO]):
    def __init__(
        self,
        auth_repository: UserRepository,
        id_provider: IdProvider,
    ):
        self.auth_repository = auth_repository
        self.id_provider = id_provider

    async def _get_current_user(self) -> DBUser:
        """Get current user from JWT"""

        user_id = self.id_provider.get_current_user_id()

        user: Optional[DBUser] = await self.auth_repository.get(user_id)

        if not user:
            raise IsNotAuthorizedError()

        return user

    async def __call__(self, data: GetUserInputDTO) -> DBUserDTO:
        user = await self._get_current_user()

        return DBUserDTO(
            user_id=user.user_id.to_raw(),
            email=user.email.to_raw(),
            first_name=user.first_name.to_raw(),
            last_name=user.last_name.to_raw(),
            joined_at=user.joined_at.to_raw(),
        )
