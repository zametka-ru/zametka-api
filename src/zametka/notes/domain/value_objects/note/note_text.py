from dataclasses import dataclass

from zametka.notes.domain.common.value_objects.base import ValueObject
from zametka.notes.domain.exceptions.note import InvalidNoteTextError


@dataclass(frozen=True)
class NoteText(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if len(self.value) > 60000:
            raise InvalidNoteTextError("Текст заметки слишком длинный!")
        if not self.value:
            raise InvalidNoteTextError("Текст заметки пуст!")
