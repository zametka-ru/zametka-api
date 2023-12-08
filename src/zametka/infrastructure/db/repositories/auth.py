from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from zametka.application.auth.dto import UserDTO
from zametka.application.common.repository import (
    AuthRepository,
)

from zametka.domain.entities.user import User as UserEntity, DBUser
from zametka.domain.value_objects.user.user_email import UserEmail
from zametka.domain.value_objects.user.user_id import UserId

from zametka.infrastructure.db import User
from zametka.infrastructure.db.converters.user import (
    user_db_model_to_user_dto,
    user_db_model_to_db_user_entity,
    user_entity_to_db_model,
)


class AuthRepositoryImpl(AuthRepository):
    """Repository of auth part of app"""

    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        user: UserEntity,
    ) -> UserDTO:
        """Register user"""

        db_user = user_entity_to_db_model(user)

        self.session.add(db_user)

        return user_db_model_to_user_dto(db_user)

    async def get(self, user_id: UserId) -> Optional[DBUser]:
        """Get user by id"""

        q = select(User).where(User.id == user_id.to_raw())

        res = await self.session.execute(q)
        user: Optional[User] = res.scalar()

        if not user:
            return None

        return user_db_model_to_db_user_entity(user)

    async def get_by_email(self, email: UserEmail) -> Optional[DBUser]:
        """Get user by email"""

        q = select(User).where(User.email == email.to_raw())

        res = await self.session.execute(q)

        user: Optional[User] = res.scalar()

        if not user:
            return None

        return user_db_model_to_db_user_entity(user)

    async def set_active(self, user_id: UserId) -> None:
        """
        Set user.is_active to True
        """

        q = update(User).where(User.id == user_id.to_raw()).values(is_active=True)

        await self.session.execute(q)
