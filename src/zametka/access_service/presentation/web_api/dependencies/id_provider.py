from fastapi import Depends
from fastapi_another_jwt_auth import AuthJWT

from zametka.access_service.application.common.id_provider import IdProvider
from zametka.access_service.infrastructure.id_provider import (
    TokenIdProvider,
    JWTTokenProcessor,
)


def get_token_id_provider(
    jwt_auth: AuthJWT = Depends(),
) -> IdProvider:
    jwt_auth.jwt_required()

    token_processor = JWTTokenProcessor(token_processor=jwt_auth)
    id_provider = TokenIdProvider(token_processor=token_processor)

    return id_provider
