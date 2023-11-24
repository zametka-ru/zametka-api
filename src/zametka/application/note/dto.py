from dataclasses import dataclass
from typing import Optional

from zametka.domain.entities.note import Note
from zametka.domain.value_objects.note_id import NoteId


@dataclass(frozen=True)
class CreateNoteInputDTO:
    title: str
    text: str


@dataclass(frozen=True)
class CreateNoteOutputDTO:
    note: Note


@dataclass(frozen=True)
class UpdateNoteInputDTO:
    note_id: NoteId
    title: str
    text: str


@dataclass(frozen=True)
class UpdateNoteOutputDTO:
    note: Note


@dataclass(frozen=True)
class ReadNoteInputDTO:
    note_id: NoteId


@dataclass(frozen=True)
class ReadNoteOutputDTO:
    note: Note


@dataclass(frozen=True)
class ListNotesInputDTO:
    page: int
    search: Optional[str] = None


@dataclass(frozen=True)
class ListNotesOutputDTO:
    notes: list[Note]


@dataclass(frozen=True)
class DeleteNoteInputDTO:
    note_id: NoteId


@dataclass(frozen=True)
class DeleteNoteOutputDTO:
    pass
