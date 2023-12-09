from abc import abstractmethod
from typing import Optional, Protocol

from zametka.application.user.dto import UserDTO
from zametka.application.note.dto import ListNotesDTO, NoteDTO, DBNoteDTO
from zametka.domain.entities.note import Note, DBNote
from zametka.domain.entities.user import User, DBUser
from zametka.domain.value_objects.note.note_id import NoteId
from zametka.domain.value_objects.user.user_email import UserEmail
from zametka.domain.value_objects.user.user_id import UserId


class UserRepository(Protocol):
    """User repository interface"""

    @abstractmethod
    async def create(self, user: User) -> UserDTO:
        """Create"""

    @abstractmethod
    async def get(self, user_id: UserId) -> Optional[DBUser]:
        """Get by id"""

    @abstractmethod
    async def get_by_email(self, email: UserEmail) -> Optional[DBUser]:
        """Get by email"""

    @abstractmethod
    async def update(self, user_id: UserId, updated_user: DBUser) -> None:
        """Update"""


class NoteRepository(Protocol):
    """Note repository interface"""

    @abstractmethod
    async def create(self, note: Note) -> NoteDTO:
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
    async def list(self, limit: int, offset: int, author_id: UserId) -> ListNotesDTO:
        """List"""

    @abstractmethod
    async def search(self, query: str, limit: int, offset: int) -> ListNotesDTO:
        """FTS"""

    @abstractmethod
    async def delete(self, note_id: NoteId) -> None:
        """Delete"""
