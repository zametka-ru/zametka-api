from abc import abstractmethod
from typing import Generic

from zametka.access_service.application.common.event.event import EventT


class EventHandler(Generic[EventT]):
    @abstractmethod
    async def __call__(self, event: EventT) -> None:
        """Event handler"""
        raise NotImplementedError
