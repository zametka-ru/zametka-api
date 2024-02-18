from datetime import datetime, timezone
from uuid import uuid4

import pytest

from tests.mocks.access_service.user_identity_repository import (
    FakeUserIdentityRepository,
)
from tests.mocks.access_service.uow import FakeUoW

from zametka.access_service.application.verify_email import VerifyEmail, TokenInputDTO
from zametka.access_service.domain.entities.confirmation_token import (
    IdentityConfirmationToken,
)
from zametka.access_service.domain.entities.user_identity import UserIdentity
from zametka.access_service.domain.exceptions.user_identity import UserIsNotExistsError

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


@pytest.mark.skip(reason="Helper function")
def get_token_with_incorrect_uid() -> IdentityConfirmationToken:
    return IdentityConfirmationToken(uid=UserIdentityId(uuid4()))


async def test_verify_email(
    user_identity_repository: FakeUserIdentityRepository,
    uow: FakeUoW,
) -> None:
    assert user_identity_repository.user.is_active is False

    interactor = VerifyEmail(
        user_repository=user_identity_repository,
        uow=uow,
    )

    token = IdentityConfirmationToken(uid=user_identity_repository.user.identity_id)

    dto = TokenInputDTO(
        uid=token.uid.to_raw(),
        timestamp=datetime.now(tz=timezone.utc),
    )

    result = await interactor(dto)

    assert result is None
    assert uow.committed is True
    assert user_identity_repository.user.is_active is True


async def test_verify_incorrect_email(
    user_identity_repository: FakeUserIdentityRepository,
    uow: FakeUoW,
) -> None:
    assert user_identity_repository.user.is_active is False

    interactor = VerifyEmail(
        user_repository=user_identity_repository,
        uow=uow,
    )

    token = get_token_with_incorrect_uid()

    dto = TokenInputDTO(
        uid=token.uid.to_raw(),
        timestamp=datetime.now(tz=timezone.utc),
    )

    with pytest.raises(UserIsNotExistsError):
        await interactor(dto)
