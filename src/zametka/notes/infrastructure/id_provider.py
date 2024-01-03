from zametka.notes.infrastructure.access_api_client import AccessAPIClient
from zametka.notes.application.common.id_provider import IdProvider

from zametka.notes.domain.value_objects.user.user_identity_id import UserIdentityId


class RawIdProvider(IdProvider):
    def __init__(self, user_id: UserIdentityId) -> None:
        self._user_id = user_id

    async def get_identity_id(self) -> UserIdentityId:
        return self._user_id


class TokenIdProvider(IdProvider):
    def __init__(self, api_client: AccessAPIClient):
        self._api_client = api_client

    async def get_identity_id(self) -> UserIdentityId:
        user_id = await self._api_client.get_identity()

        return user_id
