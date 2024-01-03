from zametka.access_service.domain.entities.user_identity import (
    UserIdentity as UserEntity,
)

from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_hashed_password import (
    UserHashedPassword,
)
from zametka.access_service.domain.value_objects.user_identity_id import UserIdentityId

from zametka.access_service.infrastructure.db.models.user_identity import UserIdentity
from zametka.access_service.application.dto import UserIdentityDTO


def user_model_to_entity(user: UserIdentity) -> UserEntity:
    return UserEntity(
        identity_id=UserIdentityId(user.identity_id),
        email=UserEmail(user.email),
        is_active=user.is_active,
        hashed_password=UserHashedPassword(user.password),
    )


def user_model_to_dto(user: UserIdentity) -> UserIdentityDTO:
    return UserIdentityDTO(
        identity_id=user.identity_id,
    )


def user_entity_to_model(user: UserEntity) -> UserIdentity:
    db_user = UserIdentity(
        identity_id=user.identity_id.to_raw(),
        email=user.email.to_raw(),
        password=user.hashed_password.to_raw(),
        is_active=user.is_active,
    )

    return db_user
