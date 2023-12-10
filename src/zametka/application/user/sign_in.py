from dataclasses import dataclass
from typing import Optional

from zametka.domain.value_objects.user.user_email import UserEmail
from zametka.application.common.interactor import Interactor
from zametka.application.common.repository import (
    UserRepository,
)

from zametka.domain.entities.user import DBUser
from zametka.domain.exceptions.user import (
    UserIsNotExistsError,
)
from zametka.domain.services.user_service import UserService
from zametka.domain.value_objects.user.user_raw_password import UserRawPassword


@dataclass(frozen=True)
class SignInInputDTO:
    email: str
    password: str


@dataclass(frozen=True)
class SignInOutputDTO:
    user_id: int


class SignIn(Interactor[SignInInputDTO, SignInOutputDTO]):
    def __init__(
        self,
        user_repository: UserRepository,
        user_service: UserService,
    ):
        self.user_repository = user_repository
        self.user_service = user_service

    async def __call__(self, data: SignInInputDTO) -> SignInOutputDTO:
        user: Optional[DBUser] = await self.user_repository.get_by_email(
            UserEmail(data.email)
        )

        if not user:
            raise UserIsNotExistsError()

        self.user_service.ensure_can_login(user, UserRawPassword(data.password))

        user_id = user.user_id

        return SignInOutputDTO(
            user_id=user_id.to_raw(),
        )
