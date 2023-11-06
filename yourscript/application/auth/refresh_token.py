from dataclasses import dataclass

from application.common.adapters import JWT
from application.common.interactor import Interactor
from application.common.repository import RefreshTokenRepository, AuthRepository
from application.common.uow import UoW

from domain.entities.refresh_token import RefreshToken
from domain.entities.user import User
from domain.value_objects.user_id import UserId


@dataclass
class RefreshTokenInputDTO:
    refresh: RefreshToken


@dataclass
class RefreshTokenOutputDTO:
    access: str
    refresh: str


class RefreshTokenInteractor(Interactor[RefreshTokenInputDTO, RefreshTokenOutputDTO]):
    def __init__(
        self,
        token_repository: RefreshTokenRepository,
        auth_repository: AuthRepository,
        jwt: JWT,
        uow: UoW,
    ):
        self.uow = uow
        self.jwt = jwt
        self.token_repository = token_repository
        self.auth_repository = auth_repository

    async def __call__(self, data: RefreshTokenInputDTO) -> RefreshTokenOutputDTO:
        refresh_exists = await self.token_repository.exists(data.refresh.token)

        if not refresh_exists:
            raise ValueError("Invalid refresh token")

        user_id: UserId = UserId(int(self.jwt.get_jwt_subject()))

        user: User = await self.auth_repository.get(user_id)

        access = self.jwt.create_access_token(subject=str(user.user_id))
        refresh = self.jwt.create_refresh_token(subject=str(user.user_id))

        await self.token_repository.delete(user.user_id)
        await self.token_repository.create(
            RefreshToken(
                token=refresh,
                user_id=user.user_id,
            )
        )

        await self.uow.commit()

        return RefreshTokenOutputDTO(
            access=access,
            refresh=refresh,
        )
