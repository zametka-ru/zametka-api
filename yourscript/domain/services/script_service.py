import datetime

from domain.entities import Script
from domain.value_objects.user_id import UserId


class ScriptService:

    def create(self, title: str, text: str, user_id: UserId) -> Script:
        return Script(
            title=title, text=text, author_id=user_id, created_at=datetime.datetime.now()
        )

    def has_access(self, script: Script, user_id: UserId) -> bool:
        return script.author_id == user_id
