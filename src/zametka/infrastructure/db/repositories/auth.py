from typing import Optional

from sqlalchemy import select, update

from zametka.application.common.repository import (
    AuthRepository,
)

from zametka.domain.entities.user import DBUser
from zametka.domain.entities.user import User as UserEntity
from zametka.domain.value_objects.user_id import UserId
from zametka.infrastructure.db import User


class AuthRepositoryImpl(AuthRepository):
    """Repository of auth part of app"""

    async def create(
        self,
        user: UserEntity,
    ) -> UserEntity:
        """Register user"""

        db_user = User(
            email=user.email,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
            joined_at=user.joined_at,
            is_superuser=user.is_superuser,
            is_active=user.is_active,
        )

        self.session.add(db_user)

        return UserEntity(
            email=db_user.email,
            password=db_user.password,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            joined_at=db_user.joined_at,
            is_superuser=db_user.is_superuser,
            is_active=db_user.is_active,
        )

    async def get(self, user_id: UserId) -> DBUser:
        """Get user by id"""

        q = select(User).where(User.id == int(user_id))

        res = await self.session.execute(q)
        user: User = res.scalar()

        return DBUser(
            user_id=user.id,
            email=user.email,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
            joined_at=user.joined_at,
            is_superuser=user.is_superuser,
            is_active=user.is_active,
        )

    async def get_by_email(self, email: str) -> Optional[DBUser]:
        """Get user by email"""

        q = select(User).where(User.email == email)

        res = await self.session.execute(q)

        user: User = res.scalar()

        if not user:
            return None

        return DBUser(
            user_id=user.id,
            email=user.email,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
            joined_at=user.joined_at,
            is_superuser=user.is_superuser,
            is_active=user.is_active,
        )

    async def set_active(self, user_id: UserId) -> None:
        """
        Set user.is_active to True
        """

        q = update(User).where(User.id == user_id).values(is_active=True)

        await self.session.execute(q)
