from sqlalchemy.ext.asyncio import AsyncSession

from application.common.repository import AuthRepository, ScriptRepository

from infrastructure.db.uow import UnitOfWork


def get_uow(session: AsyncSession):
    return UnitOfWork(session=session)


def get_auth_repository(session: AsyncSession):
    return AuthRepository(session=session)


def get_script_repository(session: AsyncSession):
    return ScriptRepository(session=session)
