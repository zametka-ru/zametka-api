import jwt

from application.common.adapters import JWTOperations


class JWTOperationsImpl(JWTOperations):
    """JWTOpsInterface implementation"""

    def encode(self, payload: dict, secret_key: str, algorithm: str) -> str:
        return str(jwt.encode(payload, secret_key, algorithm))[2:-1]

    def decode(self, token: str, secret_key: str, algorithm: list[str]) -> dict:
        return jwt.decode(token, secret_key, algorithm)
