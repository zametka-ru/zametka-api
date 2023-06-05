from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.settings import DB


async def get_async_sessionmaker(settings: DB) -> sessionmaker:
    """Get async sessionmaker"""

    engine = create_async_engine(
        settings.get_connection_url(),
        future=True,
    )

    # noinspection PyTypeChecker
    async_sessionmaker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )  # type:ignore

    return async_sessionmaker
