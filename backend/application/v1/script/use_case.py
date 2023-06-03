from sqlalchemy.exc import DBAPIError

from .dto import CreateScriptInputDTO

from adapters.repository.script import ScriptRepository
from adapters.repository.auth import AuthRepository
from adapters.v1.script import get_current_user

from presentation.v1.schemas.script import (
    CreateScriptFailedResponse,
    CreateScriptSuccessResponse,
)

from adapters.repository.uow import UnitOfWork

from fastapi_jwt_auth import AuthJWT


async def create_script_case(
    dto: CreateScriptInputDTO,
    repository: ScriptRepository,
    auth_repository: AuthRepository,
    uow: UnitOfWork,
    Authorize: AuthJWT,
):
    """Create script use case"""

    try:
        user = await get_current_user(Authorize, auth_repository)

        script = await repository.create_script(
            user=user,
            title=dto.script_title,
            text=dto.script_text,
            created_at=dto.script_created_at,
        )

        await uow.commit()

    except DBAPIError as exc:
        return CreateScriptFailedResponse(details=exc, code=400)

    return CreateScriptSuccessResponse(script=script)
