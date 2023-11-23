from yourscript.application.common.adapters import JWT
from yourscript.application.common.id_provider import IdProvider

from yourscript.domain.value_objects.user_id import UserId


class TokenIdProvider(IdProvider):
    def __init__(
        self,
        token_processor: JWT,
    ):
        self.token_processor = token_processor

    def get_current_user_id(self) -> UserId:
        user_id = UserId(self.token_processor.get_jwt_subject())

        return user_id