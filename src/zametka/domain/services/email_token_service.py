from datetime import datetime, timezone, timedelta
from typing import TypeAlias

from zametka.domain.entities.user import User, DBUser
from zametka.domain.exceptions.email_token import (
    CorruptedEmailTokenError,
    EmailTokenAlreadyUsedError,
)
from zametka.domain.exceptions.user import UserIsNotExistsError

Payload: TypeAlias = dict[str, datetime | str | bool]


class EmailTokenService:
    def encode_payload(self, user: User) -> Payload:
        exp: datetime = datetime.now(tz=timezone.utc) + timedelta(minutes=15)

        payload: Payload = {
            "user_email": user.email.to_raw(),
            "exp": exp,
            "user_is_active": user.is_active,
        }

        return payload

    def check_payload(self, user: DBUser, payload: Payload) -> DBUser:
        if not user:
            raise UserIsNotExistsError()

        token_user_is_active = payload.get("user_is_active")

        if token_user_is_active is None:
            raise CorruptedEmailTokenError()

        if user.is_active != token_user_is_active:
            raise EmailTokenAlreadyUsedError()

        return user
