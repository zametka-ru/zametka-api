from zametka.access_service.application.common.id_provider import UserProvider
from zametka.access_service.domain.entities.user_identity import UserIdentity
from zametka.access_service.domain.value_objects.user_identity_id import UserIdentityId


class FakeUserProvider(UserProvider):
    def __init__(self, user: UserIdentity):
        self.requested = False
        self.user = user

    def get_identity_id(self) -> UserIdentityId:
        if self.requested:
            raise ValueError("Identity requested twice! Please, check your interactor.")

        self.requested = True
        return self.user.identity_id

    async def get_user(self) -> UserIdentity:
        if self.requested:
            raise ValueError("Identity requested twice! Please, check your interactor.")

        self.requested = True
        return self.user
