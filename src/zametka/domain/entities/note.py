from dataclasses import dataclass
from datetime import datetime

from zametka.domain.value_objects.user_id import UserId


@dataclass
class Note:
    title: str
    text: str
    created_at: datetime
    author_id: UserId
