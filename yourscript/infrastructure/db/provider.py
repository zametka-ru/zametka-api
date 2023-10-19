from fastapi import Depends

from sqlalchemy.orm import sessionmaker, Session

from infrastructure.db.repositories.auth import AuthRepository
from infrastructure.db.repositories.script import ScriptRepository

from infrastructure.db.uow import UnitOfWork

from infrastructure.stubs import SessionStub


def get_uow(session: SessionStub = Depends()):
    yield UnitOfWork(session=session)


def get_auth_repository(session: SessionStub = Depends()):
    yield AuthRepository(session=session)


def get_script_repository(session: SessionStub = Depends()):
    yield ScriptRepository(session=session)


class DbProvider:
    """Database session management"""

    def __init__(self, pool: sessionmaker):
        self.pool = pool

    async def get_session(self) -> Session:
        """Get session"""

        async with self.pool() as session:
            yield session
