import jwt

from datetime import datetime, timezone, timedelta
from typing import TypeAlias

from zametka.domain.entities.user import User, DBUser
from zametka.domain.exceptions.email_token import (
    CorruptedEmailTokenError,
    EmailTokenAlreadyUsedError,
)
from zametka.domain.exceptions.user import UserIsNotExistsError
from zametka.domain.value_objects.email_token import EmailToken

Payload: TypeAlias = dict[str, datetime | str | bool]


class EmailTokenService:
    def encode_token(self, user: User, secret_key: str, algorithm: str) -> EmailToken:
        exp: datetime = datetime.now(tz=timezone.utc) + timedelta(minutes=15)

        payload: Payload = {
            "user_email": user.email.to_raw(),
            "exp": exp,
            "user_is_active": user.is_active,
        }

        token = EmailToken(jwt.encode(payload, secret_key, algorithm))

        return token

    def decode_token(
        self, token: EmailToken, secret_key: str, algorithm: str
    ) -> Payload:
        payload: Payload = jwt.decode(
            token.to_raw(), secret_key, algorithms=[algorithm]
        )

        return payload

    def activate_user(self, user: DBUser, payload: Payload) -> DBUser:
        if not user:
            raise UserIsNotExistsError()

        token_user_is_active = payload.get("user_is_active")

        if token_user_is_active is None:
            raise CorruptedEmailTokenError()

        if user.is_active != token_user_is_active:
            raise EmailTokenAlreadyUsedError()

        user.is_active = True

        return user
