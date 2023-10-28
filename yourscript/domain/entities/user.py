from dataclasses import dataclass
from datetime import datetime

from domain.value_objects.user_id import UserId


@dataclass
class User:
    email: str
    password: str
    first_name: str
    last_name: str
    joined_at: datetime
    is_superuser: bool = False
    is_active: bool = False
    user_id: UserId = None
