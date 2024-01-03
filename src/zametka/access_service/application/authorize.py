from dataclasses import dataclass
from typing import Optional

from zametka.access_service.application.dto import UserIdentityDTO
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.application.common.interactor import Interactor
from zametka.access_service.application.common.repository import (
    UserIdentityRepository,
)

from zametka.access_service.domain.entities.user_identity import UserIdentity
from zametka.access_service.domain.exceptions.user_identity import (
    UserIsNotExistsError,
)
from zametka.access_service.domain.services.user_identity_service import (
    UserIdentityService,
)
from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)


@dataclass(frozen=True)
class AuthorizeInputDTO:
    email: str
    password: str


class Authorize(Interactor[AuthorizeInputDTO, UserIdentityDTO]):
    def __init__(
        self,
        user_repository: UserIdentityRepository,
        user_service: UserIdentityService,
    ):
        self.user_repository = user_repository
        self.user_service = user_service

    async def __call__(self, data: AuthorizeInputDTO) -> UserIdentityDTO:
        user: Optional[UserIdentity] = await self.user_repository.get_by_email(
            UserEmail(data.email)
        )

        if not user:
            raise UserIsNotExistsError()

        self.user_service.ensure_can_login(user, UserRawPassword(data.password))

        return UserIdentityDTO(
            identity_id=user.identity_id.to_raw(),
        )
