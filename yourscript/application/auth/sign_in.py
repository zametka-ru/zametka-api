from dataclasses import dataclass

from application.common.adapters import JWT, PasswordHasher, HashedPassword
from application.common.interactor import Interactor
from application.common.repository import AuthRepository, RefreshTokenRepository
from application.common.uow import UoW

from domain.entities.user import User
from domain.exceptions.user import UserIsNotExists, UserIsNotActive, InvalidCredentials
from domain.services.refresh_token_service import RefreshTokenService
from domain.entities.refresh_token import RefreshToken


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
    ):
        self.uow = uow
        self.jwt = jwt
        self.pwd_context = pwd_context
        self.repository = repository
        self.token_repository = token_repository
        self.token_service = token_service

    async def __call__(self, data: SignInInputDTO) -> SignInOutputDTO:
        user: User = await self.repository.get_by_email(data.email)

        if not user:
            raise UserIsNotExists()

        if not user.is_active:
            raise UserIsNotActive()

        if not self.pwd_context.verify(data.password, HashedPassword(user.password)):
            raise InvalidCredentials()

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
