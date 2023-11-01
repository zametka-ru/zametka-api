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
    user_id: UserId


@dataclass
class RefreshTokenOutputDTO:
    access: str


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
        refresh_exists = await self.token_repository.exists(data.refresh)

        if not refresh_exists:
            raise ValueError("Invalid refresh token")

        current_user_id: UserId = data.user_id

        user: User = await self.auth_repository.get(current_user_id)

        access = self.jwt.create_access_token(subject=str(user.user_id))
        refresh = self.jwt.create_refresh_token(subject=str(user.user_id))

        # Authorize.set_access_cookies(new_access_token)
        # Authorize.set_refresh_cookies(new_refresh_token)

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
        )
