from dataclasses import dataclass

from zametka.notes.domain.common.value_objects.base import ValueObject
from zametka.notes.domain.exceptions.note import InvalidNoteTitleError


@dataclass(frozen=True)
class NoteTitle(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if len(self.value) > 50:
            raise InvalidNoteTitleError("Название заметки слишком длинное!")
        if not any(not x.isspace() for x in self.value):
            raise InvalidNoteTitleError(
                "Название заметки не может состоять только из пробелов!"
            )
        if not self.value:
            raise InvalidNoteTitleError("Название заметки пусто!")
