from typing import Union

from passlib.handlers.pbkdf2 import pbkdf2_sha256

from zametka.access_service.domain.entities.confirmation_token import (
    IdentityConfirmationToken,
)
from zametka.access_service.domain.exceptions.confirmation_token import (
    ConfirmationTokenAlreadyUsedError, CorruptedConfirmationTokenError,
)
from zametka.access_service.domain.exceptions.user_identity import (
    UserIsNotActiveError,
    InvalidCredentialsError,
)
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_hashed_password import (
    UserHashedPassword,
)
from zametka.access_service.domain.value_objects.user_identity_id import UserIdentityId
from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)


class UserIdentity:
    __slots__ = ("identity_id", "email", "hashed_password", "is_active")

    def __init__(
        self,
        user_identity_id: UserIdentityId,
        email: UserEmail,
        raw_password: UserRawPassword,
    ):
        self.hashed_password = UserHashedPassword(
            pbkdf2_sha256.hash(raw_password.to_raw())
        )
        self.identity_id = user_identity_id
        self.email = email
        self.is_active = False

    def ensure_can_access(self):
        if not self.is_active:
            raise UserIsNotActiveError()

    def ensure_passwords_match(self, raw_password: UserRawPassword) -> None:
        passwords_match = pbkdf2_sha256.verify(
            raw_password.to_raw(), self.hashed_password.to_raw()
        )

        if not passwords_match:
            raise InvalidCredentialsError()

    def _activate(self) -> None:
        self.is_active = True

    def activate(self, token: IdentityConfirmationToken) -> None:
        token.verify()

        if self.is_active:
            raise ConfirmationTokenAlreadyUsedError()
        if token.uid != self.identity_id:
            raise CorruptedConfirmationTokenError()

        self._activate()

    def __hash__(self) -> int:
        return hash(self.identity_id)

    def __eq__(self, other: Union[object, "UserIdentity"]) -> bool:
        if not isinstance(other, UserIdentity):
            return False

        return self.identity_id == other.identity_id

    def __repr__(self) -> str:
        return "{} object(id={}, is_active={})".format(
            self.__class__.__qualname__, self.identity_id, bool(self)
        )

    def __str__(self) -> str:
        return "{} <{}>".format(self.__class__.__qualname__, self.identity_id)