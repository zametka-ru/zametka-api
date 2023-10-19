from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    email: str
    password: str
    first_name: str
    last_name: str
    joined_at: datetime
    is_superuser: bool = False
    is_active: bool = False
