from dataclasses import dataclass
from typing import Optional

from yourscript.application.common.adapters import JWT, HashedPassword, PasswordHasher
from yourscript.application.common.interactor import Interactor
from yourscript.application.common.repository import (
    AuthRepository,
    RefreshTokenRepository,
)
from yourscript.application.common.uow import UoW
from yourscript.domain.entities.refresh_token import RefreshToken
from yourscript.domain.entities.user import DBUser
from yourscript.domain.exceptions.user import (
    InvalidCredentialsError,
    UserIsNotExistsError,
)
from yourscript.domain.services.refresh_token_service import RefreshTokenService
from yourscript.domain.services.user_service import UserService


@dataclass
class SignInInputDTO:
    email: str
    password: str


@dataclass
class SignInOutputDTO:
    access: str
    refresh: str


class SignIn(Interactor[SignInInputDTO, SignInOutputDTO]):
    def __init__(
        self,
        repository: AuthRepository,
        token_repository: RefreshTokenRepository,
        jwt: JWT,
        pwd_context: PasswordHasher,
        uow: UoW,
        token_service: RefreshTokenService,
        user_service: UserService,
    ):
        self.uow = uow
        self.jwt = jwt
        self.pwd_context = pwd_context
        self.repository = repository
        self.token_repository = token_repository
        self.token_service = token_service
        self.user_service = user_service

    async def __call__(self, data: SignInInputDTO) -> SignInOutputDTO:
        user: Optional[DBUser] = await self.repository.get_by_email(data.email)

        if not user:
            raise UserIsNotExistsError()

        if not self.pwd_context.verify(data.password, HashedPassword(user.password)):
            raise InvalidCredentialsError()

        self.user_service.ensure_can_login(user)

        subject = str(user.user_id)

        access_token = self.jwt.create_access_token(subject=subject)
        refresh_token = self.jwt.create_refresh_token(subject=subject)

        refresh_token_object: RefreshToken = self.token_service.create(
            refresh_token, user.user_id
        )

        await self.token_repository.delete(user.user_id)
        await self.token_repository.create(refresh_token_object)

        await self.uow.commit()

        return SignInOutputDTO(
            access=access_token,
            refresh=refresh_token,
        )
