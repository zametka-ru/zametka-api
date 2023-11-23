from sqlalchemy.ext.asyncio import AsyncSession

from yourscript.infrastructure.db.repositories.auth import (
    AuthRepositoryImpl,
)
from yourscript.infrastructure.db.repositories.script import ScriptRepositoryImpl
from yourscript.infrastructure.db.uow import SAUnitOfWork


def get_uow(session: AsyncSession):
    return SAUnitOfWork(session=session)


def get_auth_repository(session: AsyncSession):
    return AuthRepositoryImpl(session=session)


def get_script_repository(session: AsyncSession):
    return ScriptRepositoryImpl(session=session)
