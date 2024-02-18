from uuid import uuid4

import pytest

from tests.mocks.access_service.user_identity_repository import (
    FakeUserIdentityRepository,
)
from tests.mocks.access_service.uow import FakeUoW
from tests.mocks.access_service.token_sender import FakeTokenSender

from zametka.access_service.application.create_identity import (
    CreateIdentity,
    IdentityInputDTO,
)
from zametka.access_service.application.dto import UserIdentityDTO
from zametka.access_service.domain.entities.user_identity import UserIdentity
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
def uow() -> FakeUoW:
    return FakeUoW()


@pytest.fixture
def token_sender() -> FakeTokenSender:
    return FakeTokenSender()


async def test_create_identity(
    user_identity_repository: FakeUserIdentityRepository,
    uow: FakeUoW,
    token_sender: FakeTokenSender,
) -> None:
    interactor = CreateIdentity(
        user_repository=user_identity_repository,
        uow=uow,
        token_sender=token_sender,
    )

    dto = IdentityInputDTO(
        email=USER_EMAIL,
        password=USER_PASSWORD,
    )

    result = await interactor(dto)

    assert result is not None
    assert isinstance(result, UserIdentityDTO) is True

    assert uow.committed is True

    assert user_identity_repository.created is True
    assert result.identity_id == USER_ID

    assert token_sender.token_sent_cnt == 1
