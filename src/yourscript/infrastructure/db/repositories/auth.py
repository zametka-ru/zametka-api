from typing import Optional

from sqlalchemy import delete, exists, select, update

from yourscript.application.common.repository import (
    AuthRepository,
    RefreshTokenRepository,
)
from yourscript.domain.entities.refresh_token import RefreshToken as RefreshTokenEntity
from yourscript.domain.entities.user import DBUser
from yourscript.domain.entities.user import User as UserEntity
from yourscript.domain.value_objects.user_id import UserId
from yourscript.infrastructure.db import RefreshToken, User


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


class RefreshTokenRepositoryImpl(RefreshTokenRepository):
    """Repository of refresh tokens"""

    async def create(self, refresh_token: RefreshTokenEntity) -> RefreshTokenEntity:
        """Create refresh token instance"""

        refresh_obj = RefreshToken(
            user_id=refresh_token.user_id, token=refresh_token.token
        )

        self.session.add(refresh_obj)

        return refresh_token

    async def delete(self, user_id: UserId) -> None:
        """Delete all user refresh tokens"""

        q = delete(RefreshToken).where(RefreshToken.user_id == user_id)

        await self.session.execute(q)

    async def exists(self, token: RefreshTokenEntity) -> bool:
        q = select(exists().where(RefreshToken.token == token.token))

        result = await self.session.execute(q)

        return result.scalar()
