from zametka.access_service.application.dto import UserIdentityDTO
from zametka.access_service.application.common.id_provider import UserProvider
from zametka.access_service.application.common.interactor import Interactor


class GetIdentity(Interactor[None, UserIdentityDTO]):
    def __init__(
        self,
        user_provider: UserProvider,
    ):
        self.user_provider = user_provider

    async def __call__(self, data=None) -> UserIdentityDTO:  # type:ignore
        user = await self.user_provider.get_user()
        user.ensure_can_access()

        return UserIdentityDTO(
            identity_id=user.identity_id.to_raw(),
        )
