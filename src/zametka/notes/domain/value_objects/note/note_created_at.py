from dataclasses import dataclass
from datetime import datetime

from zametka.notes.domain.common.value_objects.base import ValueObject


@dataclass(frozen=True)
class NoteCreatedAt(ValueObject[datetime]):
    value: datetime
