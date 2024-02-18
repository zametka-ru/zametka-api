from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, kw_only=True)
class Message:
    message_id: UUID
    data: str = ""
    message_type: str = "message"
