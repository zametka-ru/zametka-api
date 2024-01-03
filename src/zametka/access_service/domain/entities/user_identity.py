from dataclasses import dataclass

from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_hashed_password import (
    UserHashedPassword,
)
from zametka.access_service.domain.value_objects.user_identity_id import UserIdentityId


@dataclass
class UserIdentity:
    identity_id: UserIdentityId
    email: UserEmail
    hashed_password: UserHashedPassword
    is_active: bool = False
