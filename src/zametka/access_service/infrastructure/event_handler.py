import logging

from zametka.access_service.application.common.event import (
    EventHandler,
    EventSender,
)

from zametka.access_service.application.dto import UserCreatedEvent


class UserCreatedEventHandler(EventHandler[UserCreatedEvent]):
    def __init__(self, event_sender: EventSender) -> None:
        self.event_sender = event_sender

    async def __call__(self, event: UserCreatedEvent) -> None:
        recipients = ["http://notes/users/"]
        data = {
            "data": event.additional_info,
            "identity_id": str(event.identity_id),
        }

        logging.info("Sending user created event with data: {}".format(data))

        await self.event_sender.send(data, recipients)
