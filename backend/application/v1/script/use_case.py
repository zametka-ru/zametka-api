from sqlalchemy.exc import DBAPIError

from .dto import (
    CreateScriptInputDTO,
    ReadScriptInputDTO,
    UpdateScriptInputDTO,
    DeleteScriptInputDTO,
)

from adapters.repository.script import ScriptRepository
from adapters.repository.auth import AuthRepository

from adapters.v1.script import get_current_user, check_script_access
from adapters.v1.exceptions.script import RestrictScriptAccess

from presentation.v1.schemas.script import (
    CreateScriptFailedResponse,
    CreateScriptSuccessResponse,
    ReadScriptSuccessResponse,
    ReadScriptFailedResponse,
    UpdateScriptSuccessResponse,
    UpdateScriptFailedResponse,
    DeleteScriptFailedResponse,
    DeleteScriptSuccessResponse,
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
        return CreateScriptFailedResponse(details=str(exc), code=400)

    return CreateScriptSuccessResponse(
        script={
            "id": script.id,
            "title": script.title,
            "text": script.text,
            "created_at": script.created_at,
            "author_id": script.user_id,
        }
    )


async def read_script_case(
    dto: ReadScriptInputDTO,
    Authorize: AuthJWT,
    auth_repository: AuthRepository,
    script_repository: ScriptRepository,
):
    """Read script by id use case"""

    try:
        script = await check_script_access(
            Authorize=Authorize,
            auth_repository=auth_repository,
            script_repository=script_repository,
            script_id=dto.script_id,
        )
    except RestrictScriptAccess as exc:
        return ReadScriptFailedResponse(details=str(exc), code=exc.http_error_code)

    return ReadScriptSuccessResponse(
        script={
            "id": script.id,
            "title": script.title,
            "text": script.text,
            "created_at": script.created_at,
            "author_id": script.user_id,
        }
    )


async def update_script_case(
    dto: UpdateScriptInputDTO,
    Authorize: AuthJWT,
    auth_repository: AuthRepository,
    script_repository: ScriptRepository,
    uow: UnitOfWork,
):
    """Update script by id use case"""

    try:
        script = await check_script_access(
            Authorize=Authorize,
            auth_repository=auth_repository,
            script_repository=script_repository,
            script_id=dto.script_id,
        )

        await script_repository.update_script(
            dto.script_id, dto.script_title, dto.script_text
        )
        await uow.commit()

    except RestrictScriptAccess as exc:
        return UpdateScriptFailedResponse(details=str(exc), code=exc.http_error_code)

    except DBAPIError as exc:
        return UpdateScriptFailedResponse(details=str(exc), code=400)

    return UpdateScriptSuccessResponse(
        script={
            "id": script.id,
            "title": dto.script_title,
            "text": dto.script_text,
            "created_at": script.created_at,
            "author_id": script.user_id,
        }
    )


async def delete_script_case(
    dto: DeleteScriptInputDTO,
    Authorize: AuthJWT,
    auth_repository: AuthRepository,
    script_repository: ScriptRepository,
    uow: UnitOfWork,
):
    """Delete script by id use case"""

    try:
        await check_script_access(
            Authorize=Authorize,
            auth_repository=auth_repository,
            script_repository=script_repository,
            script_id=dto.script_id,
        )

        await script_repository.delete_script(dto.script_id)
        await uow.commit()

    except RestrictScriptAccess as exc:
        return DeleteScriptFailedResponse(details=str(exc), code=exc.http_error_code)

    except DBAPIError as exc:
        return DeleteScriptFailedResponse(details=str(exc), code=400)

    return DeleteScriptSuccessResponse()
