from infrastructure.stubs import SessionStub


class UnitOfWork:
    """A thing which can do commit and rollback"""

    session: SessionStub

    def __init__(self, session: SessionStub):
        self.session = session

    async def commit(self):
        await self.session.commit()
