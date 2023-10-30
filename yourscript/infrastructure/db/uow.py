from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork:
    """A thing which can do commit and rollback"""

    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self):
        await self.session.commit()
