from abc import ABC, abstractmethod
from typing import Optional, List

from zametka.domain.entities.note import Note
from zametka.domain.entities.user import DBUser, User
from zametka.domain.value_objects.note_id import NoteId
from zametka.domain.value_objects.user_id import UserId


class AbstractRepository(ABC):
    """Abstract implementation of SA repository"""

    def __init__(self, session) -> None:
        self.session = session


class AuthRepository(AbstractRepository):
    """User repository interface"""

    @abstractmethod
    async def create(self, user: User) -> User:
        """Create"""

    @abstractmethod
    async def get(self, user_id: UserId) -> DBUser:
        """Get by id"""

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[DBUser]:
        """Get by email"""

    @abstractmethod
    async def set_active(self, user_id: UserId) -> None:
        """Set active"""


class NoteRepository(AbstractRepository):
    """Note repository interface"""

    @abstractmethod
    async def create(self, note: Note) -> Note:
        """Create"""

    @abstractmethod
    async def get(self, note_id: NoteId) -> Optional[Note]:
        """Get by id"""

    @abstractmethod
    async def update(self, note_id: NoteId, updated_note: Note) -> Note:
        """Update"""

    @abstractmethod
    async def list(self, limit: int, offset: int, author_id: UserId) -> list[Note]:
        """List"""

    @abstractmethod
    async def search(self, query: str, limit: int, offset: int) -> List[Note]:
        """FTS"""

    @abstractmethod
    async def delete(self, note_id: NoteId) -> None:
        """Delete"""
