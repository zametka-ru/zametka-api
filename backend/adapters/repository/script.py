from core.db import Script, User
from core.db.services.scripts import create_script

from presentation.v1.schemas.script import CreateScriptSchema

from .abstract import AbstractRepository


class ScriptRepository(AbstractRepository):
    """Repository of scripts part of app"""

    async def create_script(self, script: CreateScriptSchema, user: User) -> Script:
        """Create script"""

        return await create_script(self.session, script, user)
