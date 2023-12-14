from typing import Optional

from zametka.application.common.repository import UserRepository, NoteRepository
from zametka.application.common.uow import UoW
from zametka.application.common.id_provider import IdProvider

from zametka.domain.entities.note import Note, DBNote
from zametka.domain.entities.user import DBUser
from zametka.domain.exceptions.note import (
    NoteAccessDeniedError,
    NoteNotExistsError,
)
from zametka.domain.services.note_service import NoteService
from zametka.domain.value_objects.note.note_id import NoteId

from .dto import (
    CreateNoteInputDTO,
    DeleteNoteInputDTO,
    DeleteNoteOutputDTO,
    ReadNoteInputDTO,
    ListNotesInputDTO,
    ListNotesDTO,
    UpdateNoteInputDTO,
    DBNoteDTO,
)
from zametka.domain.exceptions.user import IsNotAuthorizedError
from zametka.domain.value_objects.note.note_text import NoteText
from zametka.domain.value_objects.note.note_title import NoteTitle
from zametka.domain.services.user_service import UserService


class NoteInteractor:
    def __init__(
        self,
        note_repository: NoteRepository,
        user_repository: UserRepository,
        uow: UoW,
        note_service: NoteService,
        user_service: UserService,
        id_provider: IdProvider,
    ):
        self.uow = uow
        self.note_service = note_service
        self.user_service = user_service
        self.note_repository = note_repository
        self.user_repository = user_repository
        self.id_provider = id_provider

    async def _get_current_user(self) -> DBUser:
        """Get current user"""

        user_id = self.id_provider.get_current_user_id()

        user: Optional[DBUser] = await self.user_repository.get(user_id)

        if not user:
            raise IsNotAuthorizedError()

        self.user_service.ensure_can_access(user)

        return user

    async def _check_exists(self, note_id: NoteId) -> DBNote:
        """Raises NoteNotExists if note with given id is not exists"""

        note: Optional[DBNote] = await self.note_repository.get(note_id)

        if not note:
            raise NoteNotExistsError()

        return note

    async def _get_note(self, note_id: NoteId) -> DBNote:
        """
        Check can user do actions with this note. These are two checks.

        1. Is note exists
        2. Is user are author of this note
        """

        note: DBNote = await self._check_exists(note_id)

        user: DBUser = await self._get_current_user()

        if not self.note_service.has_access(note, user.user_id):
            raise NoteAccessDeniedError()

        return note

    async def create(self, data: CreateNoteInputDTO) -> DBNoteDTO:
        user = await self._get_current_user()

        title = NoteTitle(data.title)
        text = NoteText(data.text) if data.text else None

        note: Note = self.note_service.create(title, user.user_id, text)

        note_dto = await self.note_repository.create(note)
        await self.uow.commit()

        return note_dto

    async def read(self, data: ReadNoteInputDTO) -> DBNoteDTO:
        """Read by id use case"""

        note: DBNote = await self._get_note(data.note_id)

        return DBNoteDTO(
            title=note.title.to_raw(),
            text=note.text.to_raw() if note.text else None,
            note_id=note.note_id.to_raw(),
        )

    async def update(self, data: UpdateNoteInputDTO) -> DBNoteDTO:
        note: DBNote = await self._get_note(data.note_id)

        title = NoteTitle(data.title)
        text = NoteText(data.text) if data.text else None

        new_note: Note = self.note_service.create(title, note.author_id, text)
        updated_note: DBNote = self.note_service.edit(note, new_note)

        updated_db_note = await self.note_repository.update(data.note_id, updated_note)

        if not updated_db_note:
            raise NoteNotExistsError()

        await self.uow.commit()

        return updated_db_note

    async def list(self, data: ListNotesInputDTO) -> ListNotesDTO:
        user: DBUser = await self._get_current_user()

        offset: int = data.offset
        limit: int = data.limit

        if not data.search:
            dto: ListNotesDTO = await self.note_repository.list(
                author_id=user.user_id,
                limit=limit,
                offset=offset,
            )
        else:
            dto: ListNotesDTO = await self.note_repository.search(  # type:ignore
                query=data.search,
                limit=limit,
                offset=offset,
            )

        return ListNotesDTO(notes=dto.notes, has_next=dto.has_next)

    async def delete(self, data: DeleteNoteInputDTO) -> DeleteNoteOutputDTO:
        await self._get_note(data.note_id)

        await self.note_repository.delete(data.note_id)
        await self.uow.commit()

        return DeleteNoteOutputDTO()
