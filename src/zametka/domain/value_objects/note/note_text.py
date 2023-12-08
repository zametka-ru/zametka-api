from dataclasses import dataclass

from zametka.domain.common.value_objects.base import ValueObject
from zametka.domain.exceptions.note import InvalidNoteTextError


@dataclass(frozen=True)
class NoteText(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if len(self.value) > 60000:
            raise InvalidNoteTextError("Текст заметки слишком длинный!")
        if not self.value:
            raise InvalidNoteTextError("Текст заметки пуст!")
