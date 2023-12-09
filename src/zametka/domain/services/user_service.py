import datetime

from zametka.domain.entities.user import DBUser, User
from zametka.domain.exceptions.user import UserIsNotActiveError
from zametka.domain.value_objects.user.user_email import UserEmail
from zametka.domain.value_objects.user.user_first_name import UserFirstName
from zametka.domain.value_objects.user.user_hashed_password import UserHashedPassword
from zametka.domain.value_objects.user.user_joined_at import UserJoinedAt
from zametka.domain.value_objects.user.user_last_name import UserLastName


class UserService:
    def create(
        self,
        email: UserEmail,
        hashed_password: UserHashedPassword,
        first_name: UserFirstName,
        last_name: UserLastName,
    ) -> User:
        return User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            joined_at=UserJoinedAt(datetime.datetime.now()),
            hashed_password=hashed_password,
        )

    def ensure_can_login(self, user: DBUser) -> None:
        if not user.is_active:
            raise UserIsNotActiveError
