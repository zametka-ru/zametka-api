from datetime import datetime

from sqlalchemy import select, update, delete

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

        q = select(Script).where(Script.id == _id)

        res = await self.session.execute(q)
        script: Script = res.scalar()

        return script

    async def update_script(self, _id: int, title: str, text: str) -> None:
        """Update script fields"""

        q = (
            update(Script)
            .where(Script.id == _id)
            .values(
                title=title,
                text=text,
            )
        )

        await self.session.execute(q)

    async def delete_script(self, _id: int) -> None:
        """Delete the script by id"""

        q = delete(Script).where(Script.id == _id)

        await self.session.execute(q)
