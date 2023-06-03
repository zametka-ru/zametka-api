"""Services (queries) for the Script model"""

from sqlalchemy.orm import Session

from core.db.models.scripts import Script, User

from presentation.v1.schemas.script import CreateScriptSchema


async def create_script(
    session: Session, script: CreateScriptSchema, user: User
) -> Script:
    """
    Create script
    """

    script_obj = Script(
        title=script.title,
        text=script.text,
        created_at=script.created_at,
    )

    script_obj.user = user

    session.add(script_obj)

    return script_obj
