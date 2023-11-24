import datetime

from zametka.domain.entities.note import Note
from zametka.domain.value_objects.user_id import UserId


class NoteService:
    def create(self, title: str, text: str, user_id: UserId) -> Note:
        return Note(
            title=title,
            text=text,
            author_id=user_id,
            created_at=datetime.datetime.now(),
        )

    def has_access(self, note: Note, user_id: UserId) -> bool:
        return note.author_id == user_id
