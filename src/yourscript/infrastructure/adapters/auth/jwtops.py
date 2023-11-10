import jwt

from yourscript.application.common.adapters import JWTOperations


class JWTOperationsImpl(JWTOperations):
    """JWTOpsInterface implementation"""

    def encode(self, payload: dict, secret_key: str, algorithm: str) -> str:
        return jwt.encode(payload, secret_key, algorithm)

    def decode(self, token: str, secret_key: str, algorithm: str) -> dict:
        return jwt.decode(token, secret_key, algorithm)  # type:ignore
