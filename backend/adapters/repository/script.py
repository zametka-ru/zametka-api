from datetime import datetime

from sqlalchemy import select

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

    async def get_script_by_id(self, _id: int) -> Script:
        """Get script by id"""

        q = select(Script).where(User.id == _id)

        res = await self.session.execute(q)
        script: Script = res.scalar()

        return script
