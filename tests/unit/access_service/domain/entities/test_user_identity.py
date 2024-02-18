from datetime import timezone, datetime, timedelta
from uuid import uuid4

import pytest

from zametka.access_service.domain.entities.confirmation_token import (
    IdentityConfirmationToken,
)
from zametka.access_service.domain.entities.user_identity import UserIdentity
from zametka.access_service.domain.exceptions.confirmation_token import (
    CorruptedConfirmationTokenError,
    ConfirmationTokenAlreadyUsedError,
    ConfirmationTokenIsExpiredError,
)
from zametka.access_service.domain.exceptions.user_identity import (
    UserIsNotActiveError,
    WeakPasswordError,
    InvalidUserEmailError,
)
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_identity_id import UserIdentityId
from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)

USER_EMAIL = "mockemail@gmail.com"
USER_FAKE_PASSWORD = "fake123Apassword##"


def test_create_user():
    uid = uuid4()

    user = UserIdentity(
        email=UserEmail(USER_EMAIL),
        raw_password=UserRawPassword(USER_FAKE_PASSWORD),
        user_identity_id=UserIdentityId(uid),
    )

    user.ensure_passwords_match(UserRawPassword(USER_FAKE_PASSWORD))

    with pytest.raises(UserIsNotActiveError):
        user.ensure_can_access()

    assert user.hashed_password.to_raw() != USER_FAKE_PASSWORD
    assert user.is_active is False


def test_activate_user():
    uid = uuid4()
    token = IdentityConfirmationToken(uid=UserIdentityId(uid))
    user = UserIdentity(
        email=UserEmail(USER_EMAIL),
        raw_password=UserRawPassword(USER_FAKE_PASSWORD),
        user_identity_id=UserIdentityId(uid),
    )

    user.activate(token)

    assert user.is_active is True
    user.ensure_can_access()


def test_activate_user_bad_uid():
    fake_uid = uuid4()
    uid = uuid4()
    token = IdentityConfirmationToken(uid=UserIdentityId(fake_uid))
    user = UserIdentity(
        email=UserEmail(USER_EMAIL),
        raw_password=UserRawPassword(USER_FAKE_PASSWORD),
        user_identity_id=UserIdentityId(uid),
    )

    with pytest.raises(CorruptedConfirmationTokenError):
        user.activate(token)


def test_activate_user_twice():
    uid = uuid4()
    token = IdentityConfirmationToken(uid=UserIdentityId(uid))
    user = UserIdentity(
        email=UserEmail(USER_EMAIL),
        raw_password=UserRawPassword(USER_FAKE_PASSWORD),
        user_identity_id=UserIdentityId(uid),
    )

    user.activate(token)

    with pytest.raises(ConfirmationTokenAlreadyUsedError):
        user.activate(token)


def test_activate_user_expired_token():
    uid = uuid4()
    token = IdentityConfirmationToken.load(
        UserIdentityId(uid), datetime.now(tz=timezone.utc) - timedelta(days=1)
    )
    user = UserIdentity(
        email=UserEmail(USER_EMAIL),
        raw_password=UserRawPassword(USER_FAKE_PASSWORD),
        user_identity_id=UserIdentityId(uid),
    )

    with pytest.raises(ConfirmationTokenIsExpiredError):
        user.activate(token)


@pytest.mark.parametrize(
    "pwd",
    [
        "qwerty",
        "qwertyA",
        "qwertyA1",
    ],
)
def test_create_user_bad_password(pwd):
    with pytest.raises(WeakPasswordError):
        UserRawPassword(pwd)


@pytest.mark.parametrize(
    "email",
    [
        "abc",
        "a" * 120,
        "myawesomeemail@gmail",
        "............@gmail.com",
        "myemailgmail.com",
        "my email@gmail.com",
        "              ",
        12345,
        "my.email@gmail.com",
    ],
)
def test_create_user_bad_email(email):
    with pytest.raises(InvalidUserEmailError):
        UserEmail(str(email))
