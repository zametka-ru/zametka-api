from dataclasses import dataclass
from typing import Optional

from yourscript.domain.value_objects.user_id import UserId
from yourscript.application.common.adapters import HashedPassword, PasswordHasher
from yourscript.application.common.interactor import Interactor
from yourscript.application.common.repository import (
    AuthRepository,
)

from yourscript.domain.entities.user import DBUser
from yourscript.domain.exceptions.user import (
    InvalidCredentialsError,
    UserIsNotExistsError,
)
from yourscript.domain.services.user_service import UserService


@dataclass(frozen=True)
class SignInInputDTO:
    email: str
    password: str


@dataclass(frozen=True)
class SignInOutputDTO:
    user_id: UserId


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
        user: Optional[DBUser] = await self.repository.get_by_email(data.email)

        if not user:
            raise UserIsNotExistsError()

        if not self.pwd_context.verify(data.password, HashedPassword(user.password)):
            raise InvalidCredentialsError()

        self.user_service.ensure_can_login(user)

        user_id = user.user_id

        return SignInOutputDTO(
            user_id=user_id,
        )
