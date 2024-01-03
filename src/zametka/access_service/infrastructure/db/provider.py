from sqlalchemy.ext.asyncio import AsyncSession

from zametka.access_service.infrastructure.repositories.user_identity import (
    UserIdentityRepositoryImpl,
)
from zametka.access_service.infrastructure.db.uow import SAUnitOfWork


def get_uow(session: AsyncSession) -> SAUnitOfWork:
    return SAUnitOfWork(session=session)


def get_user_repository(session: AsyncSession) -> UserIdentityRepositoryImpl:
    return UserIdentityRepositoryImpl(session=session)
