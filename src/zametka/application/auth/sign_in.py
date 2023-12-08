from dataclasses import dataclass
from typing import Optional

from zametka.domain.value_objects.user.user_email import UserEmail
from zametka.application.common.adapters import PasswordHasher
from zametka.application.common.interactor import Interactor
from zametka.application.common.repository import (
    AuthRepository,
)

from zametka.domain.entities.user import DBUser
from zametka.domain.exceptions.user import (
    InvalidCredentialsError,
    UserIsNotExistsError,
)
from zametka.domain.services.user_service import UserService


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
        repository: AuthRepository,
        pwd_context: PasswordHasher,
        user_service: UserService,
    ):
        self.pwd_context = pwd_context
        self.repository = repository
        self.user_service = user_service

    async def __call__(self, data: SignInInputDTO) -> SignInOutputDTO:
        user: Optional[DBUser] = await self.repository.get_by_email(
            UserEmail(data.email)
        )

        if not user:
            raise UserIsNotExistsError()

        if not self.pwd_context.verify(data.password, user.hashed_password):
            raise InvalidCredentialsError()

        self.user_service.ensure_can_login(user)

        user_id = user.user_id

        return SignInOutputDTO(
            user_id=user_id.to_raw(),
        )
