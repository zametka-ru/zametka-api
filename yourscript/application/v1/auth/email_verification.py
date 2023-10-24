from dataclasses import dataclass

from typing import Optional

from application.common.adapters import JWTOperations
from application.common.interactor import Interactor
from application.common.repository import AuthRepository
from application.common.uow import UoW

from domain.v1.entities.user import User
from domain.v1.value_objects.user_id import UserId


@dataclass
class EmailVerificationInputDTO:
    token: str
    secret_key: str
    algorithm: str


@dataclass
class EmailVerificationOutputDTO:
    pass


class EmailVerification(Interactor[EmailVerificationInputDTO, EmailVerificationOutputDTO]):
    def __init__(
            self,
            repository: AuthRepository,
            uow: UoW,
            jwt: JWTOperations,
    ):
        self.uow = uow
        self.jwt = jwt
        self.repository = repository

    async def __call__(self, data: EmailVerificationInputDTO) -> EmailVerificationOutputDTO:
        secret_key: str = data.secret_key
        algorithm: str = data.algorithm

        payload: dict[str, str | int | bool] = self.jwt.decode(data.token, secret_key, algorithm)

        user_id: Optional[int] = payload.get("id")

        user: User = await self.repository.get(UserId(user_id))

        # check_email_verification_token(secret_key, algorithm, user, dto.token, jwtops)

        await self.repository.set_active(user.user_id)

        await self.uow.commit()

        return EmailVerificationOutputDTO()
