from fastapi import APIRouter, Depends

from application.common.adapters import JWT
from domain.value_objects.script_id import ScriptId
from presentation.interactor_factory import InteractorFactory
from presentation.schemas.script import (
    CreateScriptSchema,
    UpdateScriptSchema,
)

from application.script.dto import (
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
async def create(
    script: CreateScriptSchema, ioc: InteractorFactory = Depends(), jwt: JWT = Depends()
):
    """Create script object"""

    async with ioc.pick_script_interactor(jwt, lambda i: i.create) as create_script:
        result = await create_script(
            CreateScriptInputDTO(
                text=script.text,
                title=script.title,
            )
        )

        return result


@router.get("/{script_id}")
async def read(
    script_id: int, ioc: InteractorFactory = Depends(), jwt: JWT = Depends()
):
    """Read a script by id"""

    async with ioc.pick_script_interactor(jwt, lambda i: i.read) as read_script:
        result = await read_script(
            ReadScriptInputDTO(
                script_id=ScriptId(script_id),
            )
        )

        return result


@router.put("/{script_id}")
async def update(
    new_script: UpdateScriptSchema,
    script_id: int,
    ioc: InteractorFactory = Depends(),
    jwt: JWT = Depends(),
):
    """Update script by id"""

    async with ioc.pick_script_interactor(jwt, lambda i: i.update) as update_script:
        result = await update_script(
            UpdateScriptInputDTO(
                script_id=ScriptId(script_id),
                title=new_script.title,
                text=new_script.text,
            )
        )

        return result


@router.delete("/{script_id}")
async def delete(
    script_id: int, ioc: InteractorFactory = Depends(), jwt: JWT = Depends()
):
    """Delete script by id"""

    async with ioc.pick_script_interactor(jwt, lambda i: i.delete) as delete_script:
        result = await delete_script(
            DeleteScriptInputDTO(
                script_id=ScriptId(script_id),
            )
        )

        return result
