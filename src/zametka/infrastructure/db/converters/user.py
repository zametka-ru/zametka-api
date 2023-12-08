from zametka.domain.entities.user import User as UserEntity, DBUser

from zametka.domain.value_objects.user.user_email import UserEmail
from zametka.domain.value_objects.user.user_first_name import UserFirstName
from zametka.domain.value_objects.user.user_hashed_password import UserHashedPassword
from zametka.domain.value_objects.user.user_joined_at import UserJoinedAt
from zametka.domain.value_objects.user.user_last_name import UserLastName

from zametka.infrastructure.db import User

from zametka.domain.value_objects.user.user_id import UserId

from zametka.application.auth.dto import UserDTO


def user_db_model_to_db_user_entity(user: User) -> DBUser:
    return DBUser(
        user_id=UserId(user.id),
        email=UserEmail(user.email),
        first_name=UserFirstName(user.first_name),
        last_name=UserLastName(user.last_name),
        joined_at=UserJoinedAt(user.joined_at),
        is_active=user.is_active,
        hashed_password=UserHashedPassword(user.password),
    )


def user_db_model_to_user_dto(user: User) -> UserDTO:
    return UserDTO(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        joined_at=user.joined_at,
    )


def user_entity_to_db_model(user: UserEntity) -> User:
    db_user = User(
        email=user.email.to_raw(),
        password=user.hashed_password.to_raw(),
        first_name=user.first_name.to_raw(),
        last_name=user.last_name.to_raw(),
        joined_at=user.joined_at.to_raw(),
        is_superuser=user.is_superuser,
        is_active=user.is_active,
    )

    return db_user
