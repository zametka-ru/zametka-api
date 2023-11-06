from dataclasses import dataclass
from datetime import datetime


from yourscript.domain.value_objects.user_id import UserId


@dataclass
class User:
    email: str
    password: str
    first_name: str
    last_name: str
    joined_at: datetime
    is_superuser: bool = False
    is_active: bool = False


@dataclass(kw_only=True)
class DBUser(User):
    user_id: UserId
