from zametka.infrastructure.db import Note

from zametka.domain.entities.note import Note as NoteEntity
from zametka.domain.value_objects.user_id import UserId


def note_db_model_to_entity(note: Note) -> NoteEntity:
    return NoteEntity(
        title=note.title,
        text=note.text,
        created_at=note.created_at,
        author_id=UserId(note.user_id),
    )


def notes_to_entities(notes: list[Note]) -> list[NoteEntity]:
    return [note_db_model_to_entity(note[0]) for note in notes]
