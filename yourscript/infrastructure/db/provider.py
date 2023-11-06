from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.repositories.auth import (
    AuthRepositoryImpl,
    RefreshTokenRepositoryImpl,
)
from infrastructure.db.repositories.script import ScriptRepositoryImpl

from infrastructure.db.uow import SAUnitOfWork


def get_uow(session: AsyncSession):
    return SAUnitOfWork(session=session)


def get_auth_repository(session: AsyncSession):
    return AuthRepositoryImpl(session=session)


def get_script_repository(session: AsyncSession):
    return ScriptRepositoryImpl(session=session)


def get_token_repository(session: AsyncSession):
    return RefreshTokenRepositoryImpl(session)
