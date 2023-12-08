import jwt

from zametka.application.common.adapters import JWTOperations
from zametka.domain.services.email_token_service import Payload


class JWTOperationsImpl(JWTOperations):
    """JWTOpsInterface implementation"""

    def encode(self, payload: Payload, secret_key: str, algorithm: str) -> str:
        return jwt.encode(payload, secret_key, algorithm)

    def decode(self, token: str, secret_key: str, algorithm: str) -> Payload:
        return jwt.decode(token, secret_key, algorithm)  # type:ignore
