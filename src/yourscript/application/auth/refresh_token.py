from dataclasses import dataclass

from yourscript.application.common.adapters import JWT
from yourscript.application.common.interactor import Interactor
from yourscript.application.common.repository import (
    RefreshTokenRepository,
    AuthRepository,
)
from yourscript.application.common.uow import UoW

from yourscript.domain.entities.refresh_token import RefreshToken
from yourscript.domain.entities.user import DBUser
from yourscript.domain.exceptions.refresh_token import RefreshTokenNotExists
from yourscript.domain.value_objects.user_id import UserId


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
        refresh_exists = await self.token_repository.exists(data.refresh)

        if not refresh_exists:
            raise RefreshTokenNotExists()

        user_id: UserId = data.refresh.user_id
        user: DBUser = await self.auth_repository.get(user_id)

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
