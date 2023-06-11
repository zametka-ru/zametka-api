from adapters.repository.auth import AuthRepository
from adapters.repository.script import ScriptRepository

from domain.db import User, Script

from application.v1.exceptions.script import IsNotExists, RestrictScriptAccess

from core.dependencies import AuthJWTDependency


async def get_current_user(
    Authorize: AuthJWTDependency, auth_repository: AuthRepository
) -> User:
    """Get current user from JWT"""

    user_id: int = Authorize.get_jwt_subject()

    user = await auth_repository.get_user_by_id(user_id)

    return user


async def is_script_author(script: Script, user: User) -> bool:
    """Is user are script author"""

    return script.user_id == user.id


async def check_script_exists(
    script_id: int, script_repository: ScriptRepository
) -> Script:
    """Raises IsNotExists if script with given id is not exists"""

    script = await script_repository.get_script_by_id(script_id)

    if not script:
        raise IsNotExists(Script)

    return script


async def check_script_access(
    Authorize: AuthJWTDependency,
    auth_repository: AuthRepository,
    script_repository: ScriptRepository,
    script_id: int,
):
    """
    Check can user do actions with this script. These are two checks.

    1. Is script exists
    2. Is user are author of this script

    DRY
    """

    try:
        script = await check_script_exists(script_id, script_repository)
    except IsNotExists:
        raise RestrictScriptAccess("Script with given id are not exists", 400)

    user = await get_current_user(Authorize, auth_repository=auth_repository)

    if not await is_script_author(script, user):
        raise RestrictScriptAccess("You are not author of this script.", 403)

    return script
