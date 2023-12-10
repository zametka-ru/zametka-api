from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_another_jwt_auth import AuthJWT

from zametka.application.note.dto import (
    CreateNoteInputDTO,
    DeleteNoteInputDTO,
    DeleteNoteOutputDTO,
    ReadNoteInputDTO,
    ListNotesInputDTO,
    UpdateNoteInputDTO,
)
from zametka.domain.value_objects.note.note_id import NoteId
from zametka.presentation.interactor_factory import InteractorFactory
from zametka.presentation.schemas.note import NoteSchema

router = APIRouter(
    prefix="/v1/notes",
    tags=["note"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def create(  # type:ignore
    note: NoteSchema,
    ioc: InteractorFactory = Depends(),
    jwt: AuthJWT = Depends(),
):
    """Create note object"""

    jwt.jwt_required()

    async with ioc.pick_note_interactor(jwt, lambda i: i.create) as interactor:
        response = await interactor(
            CreateNoteInputDTO(
                text=note.text,
                title=note.title,
            )
        )

        return response


@router.get("/{note_id}")
async def read(  # type:ignore
    note_id: int, ioc: InteractorFactory = Depends(), jwt: AuthJWT = Depends()
):
    """Read a note by id"""

    jwt.jwt_required()

    async with ioc.pick_note_interactor(jwt, lambda i: i.read) as interactor:
        response = await interactor(
            ReadNoteInputDTO(
                note_id=NoteId(note_id),
            )
        )

        return response


@router.put("/{note_id}")
async def update(  # type:ignore
    new_note: NoteSchema,
    note_id: int,
    ioc: InteractorFactory = Depends(),
    jwt: AuthJWT = Depends(),
):
    """Update note by id"""

    jwt.jwt_required()

    async with ioc.pick_note_interactor(jwt, lambda i: i.update) as interactor:
        response = await interactor(
            UpdateNoteInputDTO(
                note_id=NoteId(note_id),
                title=new_note.title,
                text=new_note.text,
            )
        )

        return response


@router.get("/")
async def list_notes(  # type:ignore
    limit: int,
    offset: int,
    search: Optional[str] = None,
    ioc: InteractorFactory = Depends(),
    jwt: AuthJWT = Depends(),
):
    """List notes"""

    jwt.jwt_required()

    async with ioc.pick_note_interactor(jwt, lambda i: i.list) as interactor:
        response = await interactor(
            ListNotesInputDTO(
                limit=limit,
                offset=offset,
                search=search,
            )
        )

        return response


@router.delete("/{note_id}")
async def delete(
    note_id: int, ioc: InteractorFactory = Depends(), jwt: AuthJWT = Depends()
) -> DeleteNoteOutputDTO:
    """Delete note by id"""

    jwt.jwt_required()

    async with ioc.pick_note_interactor(jwt, lambda i: i.delete) as interactor:
        response = await interactor(
            DeleteNoteInputDTO(
                note_id=NoteId(note_id),
            )
        )

        return response
