from yourscript.infrastructure.db import Script

from yourscript.domain.entities.script import Script as ScriptEntity
from yourscript.domain.value_objects.user_id import UserId


def script_db_model_to_entity(script: Script) -> ScriptEntity:
    return ScriptEntity(
        title=script.title,
        text=script.text,
        created_at=script.created_at,
        author_id=UserId(script.user_id),
    )


def scripts_to_entities(scripts: list[Script]) -> list[ScriptEntity]:
    return [script_db_model_to_entity(script[0]) for script in scripts]
