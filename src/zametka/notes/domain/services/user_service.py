import datetime

from zametka.notes.domain.value_objects.user.user_identity_id import UserIdentityId
from zametka.notes.domain.entities.user import User
from zametka.notes.domain.value_objects.user.user_first_name import UserFirstName
from zametka.notes.domain.value_objects.user.user_joined_at import UserJoinedAt
from zametka.notes.domain.value_objects.user.user_last_name import UserLastName


class UserService:
    def create(
        self,
        first_name: UserFirstName,
        last_name: UserLastName,
        identity_id: UserIdentityId,
    ) -> User:
        return User(
            first_name=first_name,
            last_name=last_name,
            joined_at=UserJoinedAt(datetime.datetime.now()),
            identity_id=identity_id,
        )
