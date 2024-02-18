from uuid import uuid4

import pytest

from tests.mocks.access_service.user_identity_repository import (
    FakeUserIdentityRepository,
)
from tests.mocks.access_service.token_sender import FakeTokenSender

from zametka.access_service.application.authorize import (
    Authorize,
    AuthorizeInputDTO,
)
from zametka.access_service.application.dto import UserIdentityDTO
from zametka.access_service.domain.entities.user_identity import UserIdentity
from zametka.access_service.domain.exceptions.user_identity import (
    UserIsNotActiveError,
    UserIsNotExistsError,
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
    user = UserIdentity(
        email=UserEmail(USER_EMAIL),
        raw_password=UserRawPassword(USER_PASSWORD),
        user_identity_id=UserIdentityId(USER_ID),
    )
    user.is_active = True

    return FakeUserIdentityRepository(
        user,
    )


@pytest.fixture
def token_sender() -> FakeTokenSender:
    return FakeTokenSender()


async def test_authorize(
    user_identity_repository: FakeUserIdentityRepository,
    token_sender: FakeTokenSender,
) -> None:
    interactor = Authorize(
        user_identity_repository,
    )

    dto = AuthorizeInputDTO(
        email=USER_EMAIL,
        password=USER_PASSWORD,
    )

    result = await interactor(dto)

    assert result is not None
    assert isinstance(result, UserIdentityDTO) is True

    assert result.identity_id == user_identity_repository.user.identity_id.to_raw()


async def test_authorize_not_active(
    user_identity_repository: FakeUserIdentityRepository,
    token_sender: FakeTokenSender,
) -> None:
    user_identity_repository.user.is_active = False

    interactor = Authorize(
        user_identity_repository,
    )

    dto = AuthorizeInputDTO(
        email=USER_EMAIL,
        password=USER_PASSWORD,
    )

    with pytest.raises(UserIsNotActiveError):
        await interactor(dto)


async def test_authorize_not_exists(
    user_identity_repository: FakeUserIdentityRepository,
    token_sender: FakeTokenSender,
) -> None:
    async def fake_get(*_):
        return None

    user_identity_repository.get_by_email = fake_get

    interactor = Authorize(
        user_identity_repository,
    )

    dto = AuthorizeInputDTO(
        email=USER_EMAIL,
        password=USER_PASSWORD,
    )

    with pytest.raises(UserIsNotExistsError):
        await interactor(dto)


async def test_authorize_bad_password(
    user_identity_repository: FakeUserIdentityRepository,
    token_sender: FakeTokenSender,
) -> None:
    interactor = Authorize(
        user_identity_repository,
    )

    dto = AuthorizeInputDTO(
        email=USER_EMAIL,
        password=USER_PASSWORD + "FAKE",
    )

    with pytest.raises(InvalidCredentialsError):
        await interactor(dto)
