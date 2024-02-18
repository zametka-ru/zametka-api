from uuid import UUID

from fastapi_another_jwt_auth import AuthJWT

from zametka.access_service.application.common.id_provider import UserProvider, IdProvider
from zametka.access_service.application.common.repository import UserIdentityRepository
from zametka.access_service.domain.entities.user_identity import UserIdentity
from zametka.access_service.domain.exceptions.user_identity import IsNotAuthorizedError, UserIsNotExistsError
from zametka.access_service.domain.value_objects.user_identity_id import UserIdentityId


class JWTTokenProcessor:
    def __init__(self, token_processor: AuthJWT) -> None:
        self.token_processor = token_processor

    def get_jwt_subject(self) -> str | int | None:
        return self.token_processor.get_jwt_subject()  # type:ignore


class TokenIdProvider(IdProvider):
    def __init__(
        self,
        token_processor: JWTTokenProcessor,
    ):
        self.token_processor = token_processor
        self._user_id = None

    def _get_id(self) -> UserIdentityId:
        if self._user_id:
            return self._user_id

        subject = self.token_processor.get_jwt_subject()

        if not isinstance(subject, str):
            raise IsNotAuthorizedError()

        user_id = UserIdentityId(UUID(subject))
        self._user_id = user_id

        return user_id

    def get_identity_id(self) -> UserIdentityId:
        return self._get_id()


class UserProviderImpl(UserProvider):
    def __init__(self, id_provider: IdProvider, user_repository: UserIdentityRepository) -> None:
        self._id_provider = id_provider
        self.user_repository = user_repository

    def get_identity_id(self) -> UserIdentityId:
        return self._id_provider.get_identity_id()

    async def get_user(self) -> UserIdentity:
        user_id = self.get_identity_id()
        user = await self.user_repository.get(user_id)

        if not user:
            raise IsNotAuthorizedError() from UserIsNotExistsError()

        return user
