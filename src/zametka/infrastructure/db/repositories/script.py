from typing import Optional, List

from sqlalchemy import delete, select, update, func, text

from zametka.application.common.repository import NoteRepository
from zametka.domain.entities.note import Note as NoteEntity
from zametka.domain.value_objects.note_id import NoteId
from zametka.domain.value_objects.user_id import UserId

from zametka.infrastructure.db import Note
from zametka.infrastructure.db.converters import (
    notes_to_entities,
    note_db_model_to_entity,
)


class NoteRepositoryImpl(NoteRepository):
    """Repository of notes part of app"""

    async def create(
        self,
        note: NoteEntity,
    ) -> NoteEntity:
        """Create"""

        db_note = Note(
            title=note.title,
            text=note.text,
            created_at=note.created_at,
            user_id=note.author_id,
        )

        self.session.add(db_note)

        return note

    async def get(self, note_id: NoteId) -> Optional[NoteEntity]:
        """Get by id"""

        q = select(Note).where(Note.id == note_id)

        res = await self.session.execute(q)

        note: Note = res.scalar()

        if not note:
            return None

        return note_db_model_to_entity(note)

    async def update(self, note_id: NoteId, updated_note: NoteEntity) -> NoteEntity:
        """Update"""

        q = (
            update(Note)
            .where(Note.id == note_id)
            .values(
                title=updated_note.title,
                text=updated_note.text,
            )
        )

        await self.session.execute(q)

        return updated_note

    async def list(
        self, limit: int, offset: int, author_id: UserId
    ) -> list[NoteEntity]:
        """List"""

        q = (
            select(Note)
            .where(Note.user_id == author_id)
            .limit(limit)
            .offset(offset)
            .order_by(Note.created_at)
        )

        res = await self.session.execute(q)
        db_notes = res.all()

        return notes_to_entities(db_notes)

    async def search(self, query: str, limit: int, offset: int) -> List[NoteEntity]:
        """FTS"""

        columns = func.coalesce(Note.title, "")
        columns = columns.self_group()

        await self.session.execute(text("SET pg_trgm.similarity_threshold=0.1"))

        q = (
            select(Note, func.similarity(columns, query))
            .where(columns.bool_op("%")(query))
            .limit(limit)
            .offset(offset)
            .order_by(func.similarity(columns, query).desc())
            .order_by(Note.created_at)
        )

        db_notes = (await self.session.execute(q)).all()

        return notes_to_entities(db_notes)

    async def delete(self, note_id: NoteId) -> None:
        """Delete"""

        q = delete(Note).where(Note.id == note_id)

        await self.session.execute(q)
