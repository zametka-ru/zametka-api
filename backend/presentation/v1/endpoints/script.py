from fastapi import APIRouter, Depends, HTTPException

from fastapi_jwt_auth import AuthJWT

from presentation.v1.schemas.script import (
    CreateScriptSchema,
    CreateScriptFailedResponse,
)

from core.dependencies import (
    ScriptRepositoryDependency,
    AuthRepositoryDependency,
    UnitOfWorkDependency,
)

from adapters.repository.auth import AuthRepository
from adapters.repository.script import ScriptRepository

from application.v1.script.use_case import create_script_case
from application.v1.script.dto import CreateScriptInputDTO

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

    Authorize.jwt_required()

    dto = CreateScriptInputDTO(
        script_text=script.text,
        script_title=script.title,
        script_created_at=script.created_at,
    )

    response = await create_script_case(
        dto=dto,
        repository=repository,
        auth_repository=auth_repository,
        uow=uow,
        Authorize=Authorize,
    )

    if isinstance(response, CreateScriptFailedResponse):
        raise HTTPException(response.code, response.details)

    return response


@router.get("/{script_id}")
async def read_script(script_id: int, Authorize: AuthJWT = Depends()):
    """Read a script by id"""

    Authorize.jwt_required()


@router.patch("/{script_id}")
def update_script():
    pass


@router.delete("/{script_id}")
def delete_script():
    pass
