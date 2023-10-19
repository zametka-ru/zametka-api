import datetime

from domain.v1.entities.script import Script
from domain.v1.value_objects.user_id import UserId


class ScriptService:
    def create(self, title: str, text: str, user_id: UserId) -> Script:
        return Script(
            title=title, text=text, user_id=user_id, created_at=datetime.datetime.now()
        )
