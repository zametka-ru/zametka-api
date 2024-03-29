from abc import abstractmethod
from typing import Protocol, Optional

from zametka.notes.application.note.dto import DBNoteDTO, ListNotesDTO
from zametka.notes.application.user.dto import UserDTO
from zametka.notes.domain.entities.note import Note, DBNote
from zametka.notes.domain.entities.user import User
from zametka.notes.domain.value_objects.note.note_id import NoteId
from zametka.notes.domain.value_objects.user.user_identity_id import UserIdentityId


class NoteRepository(Protocol):
    """Note repository interface"""

    @abstractmethod
    async def create(self, note: Note) -> DBNoteDTO:
        """Create"""

    @abstractmethod
    async def get(self, note_id: NoteId) -> Optional[DBNote]:
        """Get by id"""

    @abstractmethod
    async def update(
        self, note_id: NoteId, updated_note: DBNote
    ) -> Optional[DBNoteDTO]:
        """Update"""

    @abstractmethod
    async def list(
        self, limit: int, offset: int, author_id: UserIdentityId
    ) -> ListNotesDTO:
        """List"""

    @abstractmethod
    async def search(
        self, query: str, limit: int, offset: int, author_id: UserIdentityId
    ) -> ListNotesDTO:
        """FTS"""

    @abstractmethod
    async def delete(self, note_id: NoteId) -> None:
        """Delete"""


class UserRepository(Protocol):
    """User repository interface"""

    @abstractmethod
    async def create(self, user: User) -> UserDTO:
        """Create"""

    @abstractmethod
    async def get(self, user_id: UserIdentityId) -> Optional[UserDTO]:
        """Get by id"""
