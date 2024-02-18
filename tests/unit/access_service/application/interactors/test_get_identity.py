from uuid import uuid4

import pytest

from tests.mocks.access_service.id_provider import FakeUserProvider
from tests.mocks.access_service.user_identity_repository import (
    FakeUserIdentityRepository,
)

from zametka.access_service.application.get_identity import (
    GetIdentity,
)
from zametka.access_service.application.dto import UserIdentityDTO
from zametka.access_service.domain.entities.user_identity import UserIdentity
from zametka.access_service.domain.exceptions.user_identity import UserIsNotActiveError

from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_identity_id import UserIdentityId
from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)

USER_EMAIL = "lubaskincorporation@gmail.com"
USER_PASSWORD = "someSuper123#Password"
USER_ID = uuid4()


@pytest.fixture
def user_identity_repository() -> FakeUserIdentityRepository:
    return FakeUserIdentityRepository(
        UserIdentity(
            email=UserEmail(USER_EMAIL),
            raw_password=UserRawPassword(USER_PASSWORD),
            user_identity_id=UserIdentityId(USER_ID),
        )
    )


@pytest.fixture
def user_provider(
    user_identity_repository: FakeUserIdentityRepository,
) -> FakeUserProvider:
    return FakeUserProvider(user_identity_repository.user)


async def test_get_identity(
    user_identity_repository: FakeUserIdentityRepository,
    user_provider: FakeUserProvider,
) -> None:
    user_identity_repository.user.is_active = True

    interactor = GetIdentity(
        user_provider=user_provider,
    )

    result = await interactor()

    assert result is not None
    assert isinstance(result, UserIdentityDTO) is True
    assert result.identity_id == USER_ID
    assert user_provider.requested is True


async def test_get_identity_not_active(
    user_identity_repository: FakeUserIdentityRepository,
    user_provider: FakeUserProvider,
) -> None:
    interactor = GetIdentity(
        user_provider=user_provider,
    )

    with pytest.raises(UserIsNotActiveError):
        await interactor()
