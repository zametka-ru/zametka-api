from uuid import uuid4

import pytest

from tests.mocks.access_service.event_emitter import FakeEventEmitter
from tests.mocks.access_service.id_provider import FakeUserProvider
from tests.mocks.access_service.user_identity_repository import (
    FakeUserIdentityRepository,
)
from zametka.access_service.application.delete_identity import (
    DeleteIdentity,
    DeleteIdentityInputDTO,
)

from zametka.access_service.application.dto import UserDeletedEvent
from zametka.access_service.domain.entities.user_identity import UserIdentity
from zametka.access_service.domain.exceptions.user_identity import (
    UserIsNotActiveError,
    InvalidCredentialsError,
)

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


@pytest.fixture
def event_emitter() -> FakeEventEmitter:
    return FakeEventEmitter()


async def test_delete_identity(
    user_identity_repository: FakeUserIdentityRepository,
    user_provider: FakeUserProvider,
    event_emitter: FakeEventEmitter,
) -> None:
    user_identity_repository.user.is_active = True

    interactor = DeleteIdentity(
        user_provider=user_provider,
        event_emitter=event_emitter,
        user_repository=user_identity_repository,
    )

    result = await interactor(
        DeleteIdentityInputDTO(
            password=USER_PASSWORD,
        )
    )

    assert result is None
    assert user_provider.requested is True
    assert user_identity_repository.deleted is True
    assert event_emitter.calls(UserDeletedEvent)


async def test_delete_identity_not_active(
    user_identity_repository: FakeUserIdentityRepository,
    user_provider: FakeUserProvider,
    event_emitter: FakeEventEmitter,
) -> None:
    interactor = DeleteIdentity(
        user_provider=user_provider,
        event_emitter=event_emitter,
        user_repository=user_identity_repository,
    )

    with pytest.raises(UserIsNotActiveError):
        await interactor(
            DeleteIdentityInputDTO(
                password=USER_PASSWORD,
            )
        )


async def test_delete_identity_bad_password(
    user_identity_repository: FakeUserIdentityRepository,
    user_provider: FakeUserProvider,
    event_emitter: FakeEventEmitter,
) -> None:
    user_identity_repository.user.is_active = True

    interactor = DeleteIdentity(
        user_provider=user_provider,
        event_emitter=event_emitter,
        user_repository=user_identity_repository,
    )

    with pytest.raises(InvalidCredentialsError):
        await interactor(DeleteIdentityInputDTO(password=USER_PASSWORD + "fake"))
