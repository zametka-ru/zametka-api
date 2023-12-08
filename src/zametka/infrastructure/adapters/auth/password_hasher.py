from passlib.hash import pbkdf2_sha256

from zametka.application.common.adapters import PasswordHasher
from zametka.domain.value_objects.user.user_hashed_password import UserHashedPassword


class PasswordHasherImpl(PasswordHasher):
    def hash(self, plain: str) -> UserHashedPassword:
        return UserHashedPassword(pbkdf2_sha256.hash(plain))

    def verify(self, plain: str, hashed: UserHashedPassword) -> bool:
        return pbkdf2_sha256.verify(plain, hashed.to_raw())  # type:ignore
