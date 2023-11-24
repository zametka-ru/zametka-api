from sqlalchemy.ext.asyncio import AsyncSession

from zametka.infrastructure.db.repositories.auth import (
    AuthRepositoryImpl,
)
from zametka.infrastructure.db.repositories.script import NoteRepositoryImpl
from zametka.infrastructure.db.uow import SAUnitOfWork


def get_uow(session: AsyncSession):
    return SAUnitOfWork(session=session)


def get_auth_repository(session: AsyncSession):
    return AuthRepositoryImpl(session=session)


def get_note_repository(session: AsyncSession):
    return NoteRepositoryImpl(session=session)
