from core.db import User
from core.db.services.users import create_user, get_user_by_email, make_user_active

from .abstract import AbstractRepository


class AuthRepository(AbstractRepository):
    """Repository of auth part of app"""

    async def create_user(self, user: dict) -> User:
        """Register user"""

        return await create_user(self.session, user)

    async def get_user_by_email(self, user_email: str) -> User:
        """Get user by email"""

        return await get_user_by_email(self.session, user_email)

    async def make_user_active(self, user: User):
        """
        Set user.is_active to True
        """

        return await make_user_active(user)
