from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from yourscript.infrastructure.config_loader import DB


async def get_engine(settings: DB) -> AsyncGenerator[AsyncEngine, None]:
    """Get async SA engine"""

    engine = create_async_engine(
        settings.get_connection_url(),
        future=True,
    )

    yield engine

    await engine.dispose()


async def get_async_sessionmaker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    """Get async SA sessionmaker"""

    session_factory = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    return session_factory
