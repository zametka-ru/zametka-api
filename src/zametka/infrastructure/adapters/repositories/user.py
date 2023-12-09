from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from zametka.application.user.dto import UserDTO
from zametka.application.common.repository import (
    UserRepository,
)

from zametka.domain.entities.user import User as UserEntity, DBUser
from zametka.domain.value_objects.user.user_email import UserEmail
from zametka.domain.value_objects.user.user_id import UserId

from zametka.infrastructure.db import User
from zametka.infrastructure.adapters.repositories.converters.user import (
    user_db_model_to_user_dto,
    user_db_model_to_db_user_entity,
    user_entity_to_db_model,
)


class UserRepositoryImpl(UserRepository):
    """Repository of user part of app"""

    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        user: UserEntity,
    ) -> UserDTO:
        db_user = user_entity_to_db_model(user)

        self.session.add(db_user)

        return user_db_model_to_user_dto(db_user)

    async def get(self, user_id: UserId) -> Optional[DBUser]:
        q = select(User).where(User.id == user_id.to_raw())

        res = await self.session.execute(q)
        user: Optional[User] = res.scalar()

        if not user:
            return None

        return user_db_model_to_db_user_entity(user)

    async def get_by_email(self, email: UserEmail) -> Optional[DBUser]:
        q = select(User).where(User.email == email.to_raw())

        res = await self.session.execute(q)

        user: Optional[User] = res.scalar()

        if not user:
            return None

        return user_db_model_to_db_user_entity(user)

    async def update(self, user_id: UserId, updated_user: DBUser) -> None:
        q = (
            update(User)
            .where(User.id == user_id.to_raw())
            .values(is_active=updated_user.is_active)
        )

        await self.session.execute(q)
