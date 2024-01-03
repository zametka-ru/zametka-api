from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class UserDTO:
    first_name: str
    last_name: str
    joined_at: date
