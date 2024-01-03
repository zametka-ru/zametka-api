from passlib.handlers.pbkdf2 import pbkdf2_sha256

from zametka.access_service.domain.entities.user_identity import UserIdentity
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


class UserIdentityService:
    def create(
        self,
        user_identity_id: UserIdentityId,
        email: UserEmail,
        raw_password: UserRawPassword,
    ) -> UserIdentity:
        return UserIdentity(
            identity_id=user_identity_id,
            email=email,
            hashed_password=self.hash_password(raw_password),
        )

    def hash_password(self, raw_password: UserRawPassword) -> UserHashedPassword:
        return UserHashedPassword(pbkdf2_sha256.hash(raw_password.to_raw()))

    def ensure_can_access(self, user: UserIdentity) -> None:
        if not user.is_active:
            raise UserIsNotActiveError()

    def ensure_can_login(
        self, user: UserIdentity, raw_password: UserRawPassword
    ) -> None:
        self.ensure_can_access(user)

        password_match = pbkdf2_sha256.verify(
            raw_password.to_raw(), user.hashed_password.to_raw()
        )

        if not password_match:
            raise InvalidCredentialsError()
