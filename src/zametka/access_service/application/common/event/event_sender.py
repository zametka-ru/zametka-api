import typing


class EventSender(typing.Protocol):
    async def send(self, data: dict[str, typing.Any], receivers: list[str]) -> None:
        """Send event to receivers"""
        raise NotImplementedError
