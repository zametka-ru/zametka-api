from sqlalchemy.exc import DBAPIError

from .dto import CreateScriptInputDTO

from adapters.repository.script import ScriptRepository
from adapters.repository.auth import AuthRepository
from adapters.v1.script import get_current_user

from presentation.v1.schemas.script import CreateScriptFailedResponse, CreateScriptSuccessResponse


async def create_script_case(dto: CreateScriptInputDTO, repository: ScriptRepository, auth_repository: AuthRepository):
    """Create script use case"""

    try:
        user = await get_current_user(dto.Authorize, auth_repository)

        script = await repository.create_script(dto.script_data, user)

        await dto.uow.commit()

    except DBAPIError as exc:
        return CreateScriptFailedResponse(details=exc, code=400)

    return CreateScriptSuccessResponse(script=script)
