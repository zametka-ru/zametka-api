from typing import Optional

from sqlalchemy import delete, select, update

from yourscript.application.common.repository import ScriptRepository
from yourscript.domain.entities.script import Script as ScriptEntity
from yourscript.domain.value_objects.script_id import ScriptId
from yourscript.domain.value_objects.user_id import UserId
from yourscript.infrastructure.db import Script


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
            user_id=script.author_id,
        )

        self.session.add(db_script)

        return script

    async def get(self, script_id: ScriptId) -> Optional[ScriptEntity]:
        """Get script by id"""

        q = select(Script).where(Script.id == script_id)

        res = await self.session.execute(q)

        script: Script = res.scalar()

        if not script:
            return None

        return ScriptEntity(
            title=script.title,
            text=script.text,
            created_at=script.created_at,
            author_id=UserId(script.user_id),
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
