from dataclasses import dataclass
from uuid import uuid4

from zametka.access_service.application.common.token_sender import TokenSender
from zametka.access_service.application.common.interactor import Interactor
from zametka.access_service.application.common.repository import UserIdentityRepository
from zametka.access_service.application.common.uow import UoW
from zametka.access_service.application.dto import UserIdentityDTO
from zametka.access_service.domain.entities.confirmation_token import (
    IdentityConfirmationToken,
)
from zametka.access_service.domain.entities.user_identity import UserIdentity
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_identity_id import UserIdentityId
from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)


@dataclass(frozen=True)
class IdentityInputDTO:
    email: str
    password: str


class CreateIdentity(Interactor[IdentityInputDTO, UserIdentityDTO]):
    def __init__(
        self,
        user_repository: UserIdentityRepository,
        token_sender: TokenSender,
        uow: UoW,
    ):
        self.uow = uow
        self.token_sender = token_sender
        self.user_repository = user_repository

    async def __call__(self, data: IdentityInputDTO) -> UserIdentityDTO:
        email = UserEmail(data.email)
        raw_password = UserRawPassword(data.password)
        user_identity_id = UserIdentityId(value=uuid4())

        user = UserIdentity(
            user_identity_id,
            email,
            raw_password,
        )

        user_dto = await self.user_repository.create(user)
        await self.uow.commit()

        token: IdentityConfirmationToken = IdentityConfirmationToken(user.identity_id)

        await self.token_sender.send(token, user)

        return user_dto
