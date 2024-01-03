from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from zametka.access_service.application.dto import UserIdentityDTO
from zametka.access_service.application.common.repository import (
    UserIdentityRepository,
)

from zametka.access_service.domain.entities.user_identity import (
    UserIdentity as UserEntity,
)
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_identity_id import UserIdentityId

from zametka.access_service.infrastructure.db.models.user_identity import UserIdentity
from zametka.access_service.infrastructure.repositories.converters.user import (
    user_model_to_dto,
    user_model_to_entity,
    user_entity_to_model,
)


class UserIdentityRepositoryImpl(UserIdentityRepository):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        user: UserEntity,
    ) -> UserIdentityDTO:
        db_user = user_entity_to_model(user)

        self.session.add(db_user)

        await self.session.flush(objects=[db_user])

        return user_model_to_dto(db_user)

    async def get(self, user_id: UserIdentityId) -> Optional[UserEntity]:
        q = select(UserIdentity).where(UserIdentity.identity_id == user_id.to_raw())

        res = await self.session.execute(q)
        user: Optional[UserIdentity] = res.scalar()

        if not user:
            return None

        return user_model_to_entity(user)

    async def get_by_email(self, email: UserEmail) -> Optional[UserEntity]:
        q = select(UserIdentity).where(UserIdentity.email == email.to_raw())

        res = await self.session.execute(q)

        user: Optional[UserIdentity] = res.scalar()

        if not user:
            return None

        return user_model_to_entity(user)

    async def update(self, user_id: UserIdentityId, updated_user: UserEntity) -> None:
        q = (
            update(UserIdentity)
            .where(UserIdentity.identity_id == user_id.to_raw())
            .values(is_active=updated_user.is_active)
        )

        await self.session.execute(q)
