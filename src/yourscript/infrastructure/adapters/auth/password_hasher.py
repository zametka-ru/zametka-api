from yourscript.application.common.adapters import PasswordHasher

from yourscript.domain.value_objects.hashed_password import HashedPassword

from passlib.hash import pbkdf2_sha256


class PasswordHasherImpl(PasswordHasher):
    def hash(self, plain: str) -> HashedPassword:
        return HashedPassword(pbkdf2_sha256.hash(plain))

    def verify(self, plain: str, hashed: HashedPassword) -> bool:
        return pbkdf2_sha256.verify(plain, hashed)
