from uuid import UUID

from fastapi_another_jwt_auth import AuthJWT

from zametka.access_service.application.common.id_provider import IdProvider
from zametka.access_service.domain.exceptions.user_identity import IsNotAuthorizedError
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

    def get_identity_id(self) -> UserIdentityId:
        subject = self.token_processor.get_jwt_subject()

        if not isinstance(subject, str):
            raise IsNotAuthorizedError()

        user_id = UserIdentityId(UUID(subject))

        return user_id
