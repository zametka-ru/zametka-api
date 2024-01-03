from dataclasses import dataclass
from typing import Optional

from zametka.notes.domain.value_objects.note.note_created_at import NoteCreatedAt
from zametka.notes.domain.value_objects.note.note_id import NoteId
from zametka.notes.domain.value_objects.note.note_text import NoteText
from zametka.notes.domain.value_objects.note.note_title import NoteTitle
from zametka.notes.domain.value_objects.user.user_identity_id import UserIdentityId


@dataclass
class Note:
    title: NoteTitle
    created_at: NoteCreatedAt
    author_id: UserIdentityId
    text: Optional[NoteText] = None


@dataclass(kw_only=True)
class DBNote(Note):
    note_id: NoteId
