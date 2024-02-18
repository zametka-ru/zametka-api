from zametka.access_service.application.common.uow import UoW


class FakeUoW(UoW):
    def __init__(self):
        self.committed = False
        self.rolled_back = False
        self.flushed = False

    async def commit(self) -> None:
        if self.rolled_back:
            raise ValueError("Cannot commit after rolling back.")
        self.committed = True

    async def rollback(self) -> None:
        if self.committed:
            raise ValueError("Cannot rollback after committing.")
        self.rolled_back = True

    async def flush(self) -> None:
        if self.flushed:
            raise ValueError("Cannot flush after flushing.")
        self.flushed = True
