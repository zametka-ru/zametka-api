from dataclasses import dataclass
from typing import Optional

from zametka.domain.value_objects.note.note_created_at import NoteCreatedAt
from zametka.domain.value_objects.note.note_id import NoteId
from zametka.domain.value_objects.note.note_text import NoteText
from zametka.domain.value_objects.note.note_title import NoteTitle
from zametka.domain.value_objects.user.user_id import UserId


@dataclass
class Note:
    title: NoteTitle
    created_at: NoteCreatedAt
    author_id: UserId
    text: Optional[NoteText] = None


@dataclass(kw_only=True)
class DBNote(Note):
    note_id: NoteId
