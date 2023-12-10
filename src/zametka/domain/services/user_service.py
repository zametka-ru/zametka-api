import datetime

from passlib.handlers.pbkdf2 import pbkdf2_sha256

from zametka.domain.entities.user import DBUser, User
from zametka.domain.exceptions.user import UserIsNotActiveError, InvalidCredentialsError
from zametka.domain.value_objects.user.user_email import UserEmail
from zametka.domain.value_objects.user.user_first_name import UserFirstName
from zametka.domain.value_objects.user.user_hashed_password import UserHashedPassword
from zametka.domain.value_objects.user.user_joined_at import UserJoinedAt
from zametka.domain.value_objects.user.user_last_name import UserLastName
from zametka.domain.value_objects.user.user_raw_password import UserRawPassword


class UserService:
    def create(
        self,
        email: UserEmail,
        raw_password: UserRawPassword,
        first_name: UserFirstName,
        last_name: UserLastName,
    ) -> User:
        return User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            joined_at=UserJoinedAt(datetime.datetime.now()),
            hashed_password=self.hash_password(raw_password),
        )

    def hash_password(self, password: UserRawPassword) -> UserHashedPassword:
        return UserHashedPassword(pbkdf2_sha256.hash(password.to_raw()))

    def ensure_can_login(self, user: DBUser, password: UserRawPassword) -> None:
        if not user.is_active:
            raise UserIsNotActiveError

        password_match = pbkdf2_sha256.verify(
            password.to_raw(), user.hashed_password.to_raw()
        )

        if not password_match:
            raise InvalidCredentialsError()
