from fastapi import Depends

from sqlalchemy.orm import sessionmaker, Session

from adapters.repository import AuthRepository, ScriptRepository
from adapters.repository.uow import UnitOfWork


def get_uow(session: Session = Depends()):
    yield UnitOfWork(session=session)


def get_auth_repository(session: Session = Depends()):
    yield AuthRepository(session=session)


def get_script_repository(session: Session = Depends()):
    yield ScriptRepository(session=session)


class DbProvider:
    """Database session management"""

    def __init__(self, pool: sessionmaker):
        self.pool = pool

    async def get_session(self) -> Session:
        """Get session"""

        async with self.pool() as session:
            yield session
