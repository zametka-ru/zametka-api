from dataclasses import dataclass
from datetime import datetime

from yourscript.application.common.id_provider import IdProvider
from yourscript.application.common.interactor import Interactor
from yourscript.application.common.repository import AuthRepository
from yourscript.domain.entities.user import DBUser


@dataclass(frozen=True)
class GetUserInputDTO:
    pass


@dataclass(frozen=True)
class GetUserOutputDTO:
    first_name: str
    last_name: str
    joined_at: datetime


class GetUser(Interactor[GetUserInputDTO, GetUserOutputDTO]):
    def __init__(
            self,
            auth_repository: AuthRepository,
            id_provider: IdProvider,
    ):
        self.auth_repository = auth_repository
        self.id_provider = id_provider

    async def _get_current_user(self) -> DBUser:
        """Get current user from JWT"""

        user_id = self.id_provider.get_current_user_id()

        user: DBUser = await self.auth_repository.get(user_id)

        return user

    async def __call__(self, data: GetUserInputDTO) -> GetUserOutputDTO:
        user = await self._get_current_user()

        return GetUserOutputDTO(
            first_name=user.first_name,
            last_name=user.last_name,
            joined_at=user.joined_at,
        )
