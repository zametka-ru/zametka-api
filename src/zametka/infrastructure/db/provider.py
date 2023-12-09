from sqlalchemy.ext.asyncio import AsyncSession

from zametka.infrastructure.adapters.repositories.user import (
    UserRepositoryImpl,
)
from zametka.infrastructure.adapters.repositories.note import NoteRepositoryImpl
from zametka.infrastructure.db.uow import SAUnitOfWork


def get_uow(session: AsyncSession) -> SAUnitOfWork:
    return SAUnitOfWork(session=session)


def get_user_repository(session: AsyncSession) -> UserRepositoryImpl:
    return UserRepositoryImpl(session=session)


def get_note_repository(session: AsyncSession) -> NoteRepositoryImpl:
    return NoteRepositoryImpl(session=session)
