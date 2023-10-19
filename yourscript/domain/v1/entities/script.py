from dataclasses import dataclass
from datetime import datetime

from domain.v1.value_objects.user_id import UserId


@dataclass
class Script:
    title: str
    text: str
    created_at: datetime
    user_id: UserId
