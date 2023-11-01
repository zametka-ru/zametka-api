from dataclasses import dataclass

from typing import Optional

from application.common.adapters import JWTOperations
from application.common.interactor import Interactor
from application.common.repository import AuthRepository
from application.common.uow import UoW

from domain.entities.user import User
from domain.value_objects.token import Token
from domain.value_objects.user_id import UserId


@dataclass
class EmailVerificationInputDTO:
    token: str


@dataclass
class EmailVerificationOutputDTO:
    pass


class EmailVerification(
    Interactor[EmailVerificationInputDTO, EmailVerificationOutputDTO]
):
    def __init__(
        self,
        repository: AuthRepository,
        uow: UoW,
        jwt_ops: JWTOperations,
        secret_key: str,
        algorithm: list[str],
    ):
        self.uow = uow
        self.jwt_ops = jwt_ops
        self.repository = repository
        self._secret_key = secret_key
        self._algorithm = algorithm

    def _jwt_already_used_check(self, token: Token, user: User) -> None:
        token_payload = self.jwt_ops.decode(token, self._secret_key, self._algorithm)

        token_user_is_active: bool = token_payload.get("user_is_active")

        if user.is_active != token_user_is_active:
            raise ValueError()

    async def __call__(
        self, data: EmailVerificationInputDTO
    ) -> EmailVerificationOutputDTO:
        secret_key: str = self._secret_key
        algorithm: list[str] = self._algorithm

        payload = self.jwt_ops.decode(data.token, secret_key, algorithm)

        user_id: Optional[int] = payload.get("id")

        user: User = await self.repository.get(UserId(user_id))

        self._jwt_already_used_check(Token(data.token), user)

        await self.repository.set_active(user.user_id)

        await self.uow.commit()

        return EmailVerificationOutputDTO()
