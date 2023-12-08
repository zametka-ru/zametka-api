from sqlalchemy.ext.asyncio import AsyncSession

from zametka.infrastructure.db.repositories.auth import (
    AuthRepositoryImpl,
)
from zametka.infrastructure.db.repositories.note import NoteRepositoryImpl
from zametka.infrastructure.db.uow import SAUnitOfWork


def get_uow(session: AsyncSession) -> SAUnitOfWork:
    return SAUnitOfWork(session=session)


def get_auth_repository(session: AsyncSession) -> AuthRepositoryImpl:
    return AuthRepositoryImpl(session=session)


def get_note_repository(session: AsyncSession) -> NoteRepositoryImpl:
    return NoteRepositoryImpl(session=session)
