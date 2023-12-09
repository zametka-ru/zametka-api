from fastapi_another_jwt_auth import AuthJWT

from zametka.application.common.id_provider import IdProvider

from zametka.domain.value_objects.user.user_id import UserId


class TokenIdProvider(IdProvider):
    def __init__(
        self,
        token_processor: AuthJWT,
    ):
        self.token_processor = token_processor

    def get_current_user_id(self) -> UserId:
        user_id = UserId(int(self.token_processor.get_jwt_subject()))

        return user_id
