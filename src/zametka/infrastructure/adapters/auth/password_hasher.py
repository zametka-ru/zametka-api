from passlib.hash import pbkdf2_sha256

from zametka.application.common.password_hasher import PasswordHasher
from zametka.domain.value_objects.user.user_hashed_password import UserHashedPassword
from zametka.domain.value_objects.user.user_raw_password import UserRawPassword


class PasswordHasherImpl(PasswordHasher):
    def hash(self, plain: UserRawPassword) -> UserHashedPassword:
        return UserHashedPassword(pbkdf2_sha256.hash(plain.to_raw()))

    def verify(self, plain: UserRawPassword, hashed: UserHashedPassword) -> bool:
        return pbkdf2_sha256.verify(plain.to_raw(), hashed.to_raw())  # type:ignore
