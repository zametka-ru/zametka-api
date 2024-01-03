from dataclasses import dataclass
from typing import Any
from uuid import UUID

from zametka.access_service.application.common.event.event import Event


@dataclass(frozen=True)
class UserIdentityDTO:
    identity_id: UUID


@dataclass(frozen=True)
class UserCreatedEvent(Event):
    identity_id: UUID
    additional_info: dict[str, Any]
