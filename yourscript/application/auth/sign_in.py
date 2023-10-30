from dataclasses import dataclass

from application.common.adapters import JWT, PasswordHasher, HashedPassword
from application.common.interactor import Interactor
from application.common.repository import AuthRepository, RefreshTokenRepository
from application.common.uow import UoW

from domain.entities.user import User
from domain.services import RefreshTokenService
from domain.entities import RefreshToken


@dataclass
class SignInInputDTO:
    email: str
    password: str


@dataclass
class SignInOutputDTO:
    access: str
    refresh: str


class SignUp(Interactor[SignInInputDTO, SignInOutputDTO]):
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
            raise ValueError(f"There is no users with email \n{data.email}")

        if not user.is_active:
            raise ValueError("Confirm your email first, or you was banned :)")

        if not self.pwd_context.verify(data.password, HashedPassword(user.password)):
            raise ValueError("Invalid credentials (check your password)")

        access_token = self.jwt.create_access_token(subject=str(user.user_id))
        refresh_token = self.jwt.create_refresh_token(subject=str(user.user_id))

        self.jwt.set_access_cookies(access_token)
        self.jwt.set_refresh_cookies(refresh_token)

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