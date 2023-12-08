import datetime
from typing import Optional

from zametka.domain.entities.note import Note, DBNote
from zametka.domain.value_objects.note.note_created_at import NoteCreatedAt
from zametka.domain.value_objects.note.note_text import NoteText
from zametka.domain.value_objects.note.note_title import NoteTitle
from zametka.domain.value_objects.user.user_id import UserId


class NoteService:
    def create(
        self, title: NoteTitle, user_id: UserId, text: Optional[NoteText] = None
    ) -> Note:
        return Note(
            title=title,
            text=text,
            author_id=user_id,
            created_at=NoteCreatedAt(datetime.datetime.now()),
        )

    def edit(self, note: DBNote, edited_note: Note) -> DBNote:
        return DBNote(
            title=edited_note.title,
            text=edited_note.text or note.text,
            author_id=note.author_id,
            created_at=note.created_at,
            note_id=note.note_id,
        )

    def has_access(self, note: Note, user_id: UserId) -> bool:
        return note.author_id == user_id
