import aiohttp

from typing import Any

from zametka.access_service.application.common.event import EventSender
from zametka.access_service.application.common.exceptions import (
    EventIsNotDeliveredError,
)


class EventSenderImpl(EventSender):
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self._session = session

    async def send(self, data: dict[str, Any], receivers: list[str]) -> None:
        async with self._session:
            for receiver in receivers:
                async with self._session.post(receiver, json=data) as response:
                    try:
                        assert 199 < response.status < 300
                    except AssertionError:
                        raise EventIsNotDeliveredError(await response.json())
