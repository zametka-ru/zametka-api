from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from presentation.v1.schemas.script import (
    CreateScriptSchema,
    UpdateScriptSchema,
)

from core.dependencies import (
    ScriptRepositoryDependency,
    AuthRepositoryDependency,
    UnitOfWorkDependency,
)

from adapters.repository.uow import UnitOfWork

from adapters.repository.auth import AuthRepository
from adapters.repository.script import ScriptRepository

from application.v1.script.use_case import (
    create_script_case,
    read_script_case,
    update_script_case,
    delete_script_case,
)
from application.v1.script.dto import (
    CreateScriptInputDTO,
    ReadScriptInputDTO,
    UpdateScriptInputDTO,
    DeleteScriptInputDTO,
)

router = APIRouter(
    prefix="/v1/script",
    tags=["script"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create")
async def create_script(
    script: CreateScriptSchema,
    repository: ScriptRepositoryDependency = Depends(),
    auth_repository: AuthRepositoryDependency = Depends(),
    Authorize: AuthJWT = Depends(),
    uow: UnitOfWorkDependency = Depends(),
):
    """Create script object"""

    repository: ScriptRepository  # type:ignore
    auth_repository: AuthRepository  # type:ignore
    uow: UnitOfWork  # type:ignore

    Authorize.jwt_required()

    dto = CreateScriptInputDTO(
        script_text=script.text,
        script_title=script.title,
    )

    response = await create_script_case(
        dto=dto,
        repository=repository,
        auth_repository=auth_repository,
        uow=uow,
        Authorize=Authorize,
    )

    return response


@router.get("/{script_id}")
async def read_script(
    script_id: int,
    Authorize: AuthJWT = Depends(),
    repository: ScriptRepositoryDependency = Depends(),
    auth_repository: AuthRepositoryDependency = Depends(),
):
    """Read a script by id"""

    repository: ScriptRepository  # type:ignore
    auth_repository: AuthRepository  # type:ignore

    Authorize.jwt_required()

    dto = ReadScriptInputDTO(script_id=script_id)

    response = await read_script_case(dto, Authorize, auth_repository, repository)

    return response


@router.put("/{script_id}")
async def update_script(
    script_update: UpdateScriptSchema,
    script_id: int,
    Authorize: AuthJWT = Depends(),
    repository: ScriptRepositoryDependency = Depends(),
    auth_repository: AuthRepositoryDependency = Depends(),
    uow: UnitOfWorkDependency = Depends(),
):
    """Update script by id"""

    repository: ScriptRepository  # type:ignore
    auth_repository: AuthRepository  # type:ignore
    uow: UnitOfWork  # type:ignore

    Authorize.jwt_required()

    dto = UpdateScriptInputDTO(
        script_id=script_id,
        script_title=script_update.title,
        script_text=script_update.text,
    )

    response = await update_script_case(
        dto, Authorize, auth_repository, repository, uow
    )

    return response


@router.delete("/{script_id}")
async def delete_script(
    script_id: int,
    Authorize: AuthJWT = Depends(),
    repository: ScriptRepositoryDependency = Depends(),
    auth_repository: AuthRepositoryDependency = Depends(),
    uow: UnitOfWorkDependency = Depends(),
):
    """Delete script by id"""

    repository: ScriptRepository  # type:ignore
    auth_repository: AuthRepository  # type:ignore
    uow: UnitOfWork  # type:ignore

    Authorize.jwt_required()

    dto = DeleteScriptInputDTO(script_id=script_id)

    response = await delete_script_case(
        dto, Authorize, auth_repository, repository, uow
    )

    return response
