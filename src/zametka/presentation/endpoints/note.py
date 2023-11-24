from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_another_jwt_auth import AuthJWT

from zametka.application.note.dto import (
    CreateNoteInputDTO,
    CreateNoteOutputDTO,
    DeleteNoteInputDTO,
    DeleteNoteOutputDTO,
    ReadNoteInputDTO,
    ReadNoteOutputDTO,
    ListNotesInputDTO,
    ListNotesOutputDTO,
    UpdateNoteInputDTO,
    UpdateNoteOutputDTO,
)
from zametka.domain.value_objects.note_id import NoteId
from zametka.presentation.interactor_factory import InteractorFactory
from zametka.presentation.schemas.note import (
    CreateNoteSchema,
    UpdateNoteSchema,
)

router = APIRouter(
    prefix="/v1/notes",
    tags=["note"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=CreateNoteOutputDTO)
async def create(
    note: CreateNoteSchema,
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


@router.get("/{note_id}", response_model=ReadNoteOutputDTO)
async def read(
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


@router.put("/{note_id}", response_model=UpdateNoteOutputDTO)
async def update(
    new_note: UpdateNoteSchema,
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


@router.get("/", response_model=ListNotesOutputDTO)
async def list_notes(
    page: int = 1,
    search: Optional[str] = None,
    ioc: InteractorFactory = Depends(),
    jwt: AuthJWT = Depends(),
):
    """List notes"""

    jwt.jwt_required()

    async with ioc.pick_note_interactor(jwt, lambda i: i.list) as interactor:
        response = await interactor(
            ListNotesInputDTO(
                page=page,
                search=search,
            )
        )

        return response


@router.delete("/{note_id}", response_model=DeleteNoteOutputDTO)
async def delete(
    note_id: int, ioc: InteractorFactory = Depends(), jwt: AuthJWT = Depends()
):
    """Delete note by id"""

    jwt.jwt_required()

    async with ioc.pick_note_interactor(jwt, lambda i: i.delete) as interactor:
        response = await interactor(
            DeleteNoteInputDTO(
                note_id=NoteId(note_id),
            )
        )

        return response
