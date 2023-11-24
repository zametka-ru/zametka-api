from typing import Optional

from zametka.application.common.repository import AuthRepository, NoteRepository
from zametka.application.common.uow import UoW
from zametka.application.common.id_provider import IdProvider

from zametka.domain.entities.note import Note
from zametka.domain.entities.user import DBUser
from zametka.domain.exceptions.note import (
    NoteAccessDeniedError,
    NoteNotExistsError,
)
from zametka.domain.services.note_service import NoteService
from zametka.domain.value_objects.note_id import NoteId

from .dto import (
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

PAGE_SIZE = 5


class NoteInteractor:
    def __init__(
        self,
        note_repository: NoteRepository,
        auth_repository: AuthRepository,
        uow: UoW,
        service: NoteService,
        id_provider: IdProvider,
    ):
        self.uow = uow
        self.service = service
        self.note_repository = note_repository
        self.auth_repository = auth_repository
        self.id_provider = id_provider

    async def _get_current_user(self) -> DBUser:
        """Get current user from JWT"""

        user_id = self.id_provider.get_current_user_id()

        user: DBUser = await self.auth_repository.get(user_id)

        return user

    async def _check_exists(self, note_id: NoteId) -> Note:
        """Raises NoteNotExists if note with given id is not exists"""

        note: Optional[Note] = await self.note_repository.get(note_id)

        if not note:
            raise NoteNotExistsError()

        return note

    async def _get_note(self, note_id: NoteId) -> Note:
        """
        Check can user do actions with this note. These are two checks.

        1. Is note exists
        2. Is user are author of this note
        """

        note: Note = await self._check_exists(note_id)

        user: DBUser = await self._get_current_user()

        if not self.service.has_access(note, user.user_id):
            raise NoteAccessDeniedError()

        return note

    async def create(self, data: CreateNoteInputDTO) -> CreateNoteOutputDTO:
        user = await self._get_current_user()

        note: Note = self.service.create(data.title, data.text, user.user_id)

        await self.note_repository.create(note)

        await self.uow.commit()

        return CreateNoteOutputDTO(note=note)

    async def read(self, data: ReadNoteInputDTO) -> ReadNoteOutputDTO:
        """Read by id use case"""

        note: Note = await self._get_note(data.note_id)

        return ReadNoteOutputDTO(note=note)

    async def update(self, data: UpdateNoteInputDTO) -> UpdateNoteOutputDTO:
        note: Note = await self._get_note(data.note_id)

        new_note: Note = self.service.create(
            data.title, data.text, note.author_id
        )

        await self.note_repository.update(data.note_id, new_note)

        await self.uow.commit()

        return UpdateNoteOutputDTO(note=new_note)

    async def list(self, data: ListNotesInputDTO) -> ListNotesOutputDTO:
        user: DBUser = await self._get_current_user()

        offset: int = data.page * PAGE_SIZE
        limit: int = PAGE_SIZE

        if not data.search:
            notes: list[Note] = await self.note_repository.list(
                author_id=user.user_id,
                limit=limit,
                offset=offset,
            )
        else:
            notes: list[Note] = await self.note_repository.search(  # type:ignore
                query=data.search,
                limit=limit,
                offset=offset,
            )

        return ListNotesOutputDTO(notes=notes)

    async def delete(self, data: DeleteNoteInputDTO) -> DeleteNoteOutputDTO:
        await self._get_note(data.note_id)

        await self.note_repository.delete(data.note_id)
        await self.uow.commit()

        return DeleteNoteOutputDTO()
