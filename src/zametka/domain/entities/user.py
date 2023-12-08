from dataclasses import dataclass

from zametka.domain.value_objects.user.user_email import UserEmail
from zametka.domain.value_objects.user.user_first_name import UserFirstName
from zametka.domain.value_objects.user.user_hashed_password import UserHashedPassword
from zametka.domain.value_objects.user.user_id import UserId
from zametka.domain.value_objects.user.user_joined_at import UserJoinedAt
from zametka.domain.value_objects.user.user_last_name import UserLastName


@dataclass
class User:
    email: UserEmail
    first_name: UserFirstName
    hashed_password: UserHashedPassword
    last_name: UserLastName
    joined_at: UserJoinedAt
    is_superuser: bool = False
    is_active: bool = False


@dataclass(kw_only=True)
class DBUser(User):
    user_id: UserId
