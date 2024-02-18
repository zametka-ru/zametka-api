from dataclasses import dataclass

from zametka.access_service.application.common.event import EventEmitter
from zametka.access_service.application.common.id_provider import UserProvider
from zametka.access_service.application.common.interactor import Interactor
from zametka.access_service.application.common.repository import (
    UserIdentityRepository,
)
from zametka.access_service.application.dto import UserDeletedEvent

from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)


@dataclass(frozen=True)
class DeleteIdentityInputDTO:
    password: str


class DeleteIdentity(Interactor[DeleteIdentityInputDTO, None]):
    def __init__(
        self,
        user_repository: UserIdentityRepository,
        user_provider: UserProvider,
        event_emitter: EventEmitter[UserDeletedEvent],
    ):
        self.user_repository = user_repository
        self.user_provider = user_provider
        self.event_emitter = event_emitter

    async def __call__(self, data: DeleteIdentityInputDTO) -> None:
        user = await self.user_provider.get_user()
        raw_password = UserRawPassword(data.password)

        user.ensure_can_access()
        user.ensure_passwords_match(raw_password)

        await self.user_repository.delete(user.identity_id)

        event = UserDeletedEvent(
            identity_id=user.identity_id.to_raw(),
        )
        await self.event_emitter.emit(event)

        return None
