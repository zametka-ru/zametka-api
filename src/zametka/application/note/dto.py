from dataclasses import dataclass
from typing import Optional

from zametka.domain.value_objects.note.note_id import NoteId


@dataclass(frozen=True)
class NoteDTO:
    title: str
    text: Optional[str]


@dataclass(frozen=True, kw_only=True)
class DBNoteDTO(NoteDTO):
    note_id: int


@dataclass(frozen=True, kw_only=True)
class ListNoteDTO:
    title: str
    note_id: int


@dataclass(frozen=True)
class CreateNoteInputDTO:
    title: str
    text: Optional[str] = None


@dataclass(frozen=True)
class UpdateNoteInputDTO:
    note_id: NoteId
    title: str
    text: Optional[str] = None


@dataclass(frozen=True)
class ReadNoteInputDTO:
    note_id: NoteId


@dataclass(frozen=True)
class ListNotesInputDTO:
    limit: int
    offset: int
    search: Optional[str] = None


@dataclass(frozen=True)
class ListNotesDTO:
    notes: list[ListNoteDTO]
    has_next: bool


@dataclass(frozen=True)
class DeleteNoteInputDTO:
    note_id: NoteId


@dataclass(frozen=True)
class DeleteNoteOutputDTO:
    pass
