from dataclasses import dataclass

from zametka.notes.domain.common.value_objects.base import ValueObject


@dataclass(frozen=True)
class NoteId(ValueObject[int]):
    value: int
