from sqlalchemy import select, update, delete

from domain.v1.value_objects.script_id import ScriptId
from infrastructure.db import Script

from domain.v1.entities.script import Script as ScriptEntity

from application.common.interfaces import ScriptRepository


class ScriptRepositoryImpl(ScriptRepository):
    """Repository of scripts part of app"""

    async def create(
        self,
        script: ScriptEntity,
    ) -> ScriptEntity:
        """Create script"""

        db_script = Script(
            title=script.title,
            text=script.text,
            created_at=script.created_at,
            user_id=script.user_id,
        )

        self.session.add(db_script)

        return script

    async def get(self, script_id: ScriptId) -> ScriptEntity:
        """Get script by id"""

        q = select(Script).where(Script.id == script_id)

        res = await self.session.execute(q)
        script: Script = res.scalar()

        return ScriptEntity(
            title=script.title,
            text=script.text,
            created_at=script.created_at,
            user_id=script.user_id,
        )

    async def update(self, script_id: ScriptId, script: ScriptEntity) -> ScriptEntity:
        """Update script fields"""

        q = (
            update(Script)
            .where(Script.id == script_id)
            .values(
                title=script.title,
                text=script.text,
            )
        )

        await self.session.execute(q)

        return script

    async def delete(self, script_id: ScriptId) -> None:
        """Delete the script by id"""

        q = delete(Script).where(Script.id == script_id)

        await self.session.execute(q)