import aiohttp

from typing import Optional

from zametka.notes.domain.exceptions.user import IsNotAuthorizedError
from zametka.notes.domain.value_objects.user.user_identity_id import UserIdentityId


class AccessAPIClient:
    def __init__(
        self,
        access_token: str,
        session: aiohttp.ClientSession,
        csrf_token: Optional[str] = None,
    ) -> None:
        self.access_token = access_token
        self.csrf_token = csrf_token
        self.session = session

    def get_access_cookies(self) -> dict[str, Optional[str]]:
        return {
            "access_token_cookie": self.access_token,
            "csrf_access_token": self.csrf_token,
        }

    async def get_identity(self) -> UserIdentityId:
        async with self.session.get(
            "http://access_service/me/", cookies=self.get_access_cookies()
        ) as response:
            json = await response.json()

            if response.status == 200:
                return UserIdentityId(json.get("identity_id"))
            else:
                raise IsNotAuthorizedError()

    async def ensure_can_edit(self, headers: dict[str, Optional[str]]) -> None:
        async with self.session.get(
            "http://access_service/ensure-can-edit/",
            headers=headers,
            cookies=self.get_access_cookies(),
        ) as response:
            if response.status != 200:
                raise IsNotAuthorizedError()
