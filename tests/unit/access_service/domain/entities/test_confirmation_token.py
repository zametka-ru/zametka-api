from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from zametka.access_service.domain.entities.confirmation_token import (
    IdentityConfirmationToken,
    EXPIRES_AFTER,
)
from zametka.access_service.domain.entities.user_identity import UserIdentity
from zametka.access_service.domain.exceptions.confirmation_token import (
    ConfirmationTokenIsExpiredError,
)
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_identity_id import UserIdentityId
from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)


@pytest.fixture
def user() -> UserIdentity:
    return UserIdentity(
        email=UserEmail("testemail@gmail.com"),
        raw_password=UserRawPassword("fakePassword12#@"),
        user_identity_id=UserIdentityId(uuid4()),
    )


def test_create_token(user: UserIdentity):
    token = IdentityConfirmationToken(
        uid=user.identity_id,
    )

    token.verify()


def test_verify_expired_token(user: UserIdentity):
    expires = datetime.now(tz=timezone.utc) - timedelta(days=EXPIRES_AFTER.days + 5)
    token = IdentityConfirmationToken.load(user.identity_id, expires)

    with pytest.raises(ConfirmationTokenIsExpiredError):
        token.verify()
