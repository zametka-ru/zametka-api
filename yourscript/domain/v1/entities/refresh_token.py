from dataclasses import dataclass

from domain.v1.value_objects.user_id import UserId


@dataclass
class RefreshToken:
    token: str
    user_id: UserId
