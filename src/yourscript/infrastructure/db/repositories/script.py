from typing import Optional, List

from sqlalchemy import delete, select, update, func, text

from yourscript.application.common.repository import ScriptRepository
from yourscript.domain.entities.script import Script as ScriptEntity
from yourscript.domain.value_objects.script_id import ScriptId
from yourscript.domain.value_objects.user_id import UserId

from yourscript.infrastructure.db import Script
from yourscript.infrastructure.db.converters import (
    scripts_to_entities,
    script_db_model_to_entity,
)


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

        return script_db_model_to_entity(script)

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

    async def list(
        self, limit: int, offset: int, author_id: UserId
    ) -> list[ScriptEntity]:
        """List scripts"""

        q = (
            select(Script)
            .where(Script.user_id == author_id)
            .limit(limit)
            .offset(offset)
            .order_by(Script.created_at)
        )

        res = await self.session.execute(q)
        db_scripts = res.all()

        return scripts_to_entities(db_scripts)

    async def search(self, query: str, limit: int, offset: int) -> List[ScriptEntity]:
        """FTS with scripts"""

        columns = func.coalesce(Script.title, "")
        columns = columns.self_group()

        await self.session.execute(text("SET pg_trgm.similarity_threshold=0.1"))

        q = (
            select(Script, func.similarity(columns, query))
            .where(columns.bool_op("%")(query))
            .limit(limit)
            .offset(offset)
            .order_by(func.similarity(columns, query).desc())
            .order_by(Script.created_at)
        )

        db_scripts = (await self.session.execute(q)).all()

        return scripts_to_entities(db_scripts)

    async def delete(self, script_id: ScriptId) -> None:
        """Delete the script by id"""

        q = delete(Script).where(Script.id == script_id)

        await self.session.execute(q)
