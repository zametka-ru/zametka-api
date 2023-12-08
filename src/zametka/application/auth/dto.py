from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class UserDTO:
    email: str
    first_name: str
    last_name: str
    joined_at: date


@dataclass(frozen=True, kw_only=True)
class DBUserDTO(UserDTO):
    user_id: int
