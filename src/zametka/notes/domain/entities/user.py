from dataclasses import dataclass

from zametka.notes.domain.value_objects.user.user_first_name import UserFirstName
from zametka.notes.domain.value_objects.user.user_identity_id import UserIdentityId
from zametka.notes.domain.value_objects.user.user_joined_at import UserJoinedAt
from zametka.notes.domain.value_objects.user.user_last_name import UserLastName


@dataclass
class User:
    first_name: UserFirstName
    last_name: UserLastName
    joined_at: UserJoinedAt
    identity_id: UserIdentityId
