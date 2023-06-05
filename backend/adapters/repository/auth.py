from datetime import datetime

from sqlalchemy import select

from domain.db import User

from .abstract import AbstractRepository


class AuthRepository(AbstractRepository):
    """Repository of auth part of app"""

    async def create_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        joined_at: datetime,
        is_superuser: bool = False,
        is_active: bool = False,
    ) -> User:
        """Register user"""

        user_obj = User(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            joined_at=joined_at,
            is_superuser=is_superuser,
            is_active=is_active,
        )

        self.session.add(user_obj)

        return user_obj

    async def get_user_by_email(self, user_email: str) -> User:
        """Get user by email"""

        q = select(User).where(User.email == user_email)

        res = await self.session.execute(q)
        user: User = res.scalar()

        return user

    async def make_user_active(self, user: User) -> None:
        """
        Set user.is_active to True
        """

        user.is_active = True
