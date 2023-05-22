from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session

from ..settings import Settings


async def get_async_sessionmaker(settings: Settings) -> sessionmaker:
    """Get async sessionmaker"""

    print("------- SESSIONMAKER ---------------")

    engine = create_async_engine(
        settings.db.get_connection_url(),
        future=True,
    )

    async_sessionmaker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    ) # type:ignore

    return async_sessionmaker


def get_session(async_sessionmaker) -> Session:
    """Get async session"""

    session = async_sessionmaker()

    return session
