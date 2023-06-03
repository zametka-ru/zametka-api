from datetime import datetime

from core.db import Script, User

from .abstract import AbstractRepository


class ScriptRepository(AbstractRepository):
    """Repository of scripts part of app"""

    async def create_script(
        self,
        user: User,
        title: str,
        text: str,
        created_at: datetime,
    ) -> Script:
        """Create script"""

        script_obj = Script(
            title=title,
            text=text,
            created_at=created_at,
        )

        script_obj.user = user

        self.session.add(script_obj)

        return script_obj
