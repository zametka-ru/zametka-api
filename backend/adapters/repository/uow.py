from sqlalchemy.orm import Session


class UnitOfWork:
    """A thing which can do commit and rollback"""

    session: Session

    def __init__(self, session: Session):
        self.session = session

    async def commit(self):
        await self.session.commit()
