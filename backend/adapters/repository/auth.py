from datetime import datetime

from sqlalchemy import select, delete, exists

from domain.db import User, RefreshToken

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

    async def get_user_by_id(self, user_id: int) -> User:
        """Get user by id"""

        q = select(User).where(User.id == user_id)

        res = await self.session.execute(q)
        user: User = res.scalar()

        return user

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

    async def create_refresh_token(self, user_id: int, token: str) -> None:
        """Create refresh token instance"""

        refresh_obj = RefreshToken(user_id=user_id, token=token)

        self.session.add(refresh_obj)

    async def delete_user_tokens(self, user_id: int) -> None:
        """Delete all user refresh tokens"""

        q = delete(RefreshToken).where(RefreshToken.user_id == user_id)

        await self.session.execute(q)

    async def is_token_exists(self, token: str) -> bool:
        q = select(exists().where(RefreshToken.token == token))

        result = await self.session.execute(q)

        return result.scalar()
