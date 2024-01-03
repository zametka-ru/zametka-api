from abc import ABC, abstractmethod
from typing import Generic, Type

from zametka.access_service.application.common.event.event_handler import EventHandler
from zametka.access_service.application.common.event.event import EventsT


class EventEmitter(Generic[EventsT], ABC):
    """Event emitter pattern from EDP"""

    @abstractmethod
    def on(self, event_type: Type[EventsT], handler: EventHandler[EventsT]) -> None:
        """Subscribe to event"""
        raise NotImplementedError

    @abstractmethod
    async def emit(self, event: EventsT) -> None:
        """Emit event"""
        raise NotImplementedError
