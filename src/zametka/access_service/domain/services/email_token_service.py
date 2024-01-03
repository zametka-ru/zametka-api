import jwt

from datetime import datetime, timezone, timedelta
from typing import TypeAlias, Optional

from zametka.access_service.domain.entities.user_identity import UserIdentity
from zametka.access_service.domain.exceptions.email_token import (
    CorruptedEmailTokenError,
    EmailTokenAlreadyUsedError,
)
from zametka.access_service.domain.value_objects.email_token import EmailToken

Payload: TypeAlias = dict[str, datetime | dict[str, str | bool]]
PayloadKey: TypeAlias = Optional[str | datetime | dict[str, str | bool]]
PayloadSub: TypeAlias = dict[str, str | bool]

EXPIRES_IN = 15


class EmailTokenService:
    def encode_token(
        self, user: UserIdentity, secret_key: str, algorithm: str
    ) -> EmailToken:
        exp: datetime = datetime.now(tz=timezone.utc) + timedelta(minutes=EXPIRES_IN)

        payload: Payload = {
            "sub": {
                "email": user.email.to_raw(),
                "is_active": user.is_active,
            },
            "exp": exp,
        }

        token = EmailToken(jwt.encode(payload, secret_key, algorithm))

        return token

    def decode_token(
        self, token: EmailToken, secret_key: str, algorithm: str
    ) -> PayloadSub:
        payload: Payload = jwt.decode(
            token.to_raw(), secret_key, algorithms=[algorithm]
        )

        payload_sub: PayloadKey = payload.get("sub")

        if not payload_sub or not isinstance(payload_sub, dict):
            raise CorruptedEmailTokenError()

        is_active = payload_sub.get("is_active")
        email = payload_sub.get("email")

        if is_active is None or email is None:
            raise CorruptedEmailTokenError()

        return payload_sub

    def activate_user(
        self,
        user: UserIdentity,
        payload_sub: PayloadSub,
    ) -> UserIdentity:
        is_active = payload_sub.get("is_active")

        if user.is_active != is_active:
            raise EmailTokenAlreadyUsedError()

        user.is_active = True

        return user
