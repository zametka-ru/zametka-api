from dataclasses import dataclass

from typing import Optional

from yourscript.application.common.adapters import JWTOperations
from yourscript.application.common.interactor import Interactor
from yourscript.application.common.repository import AuthRepository
from yourscript.application.common.uow import UoW

from yourscript.domain.exceptions.user import UserIsNotExistsError
from yourscript.domain.entities.user import DBUser
from yourscript.domain.exceptions.email_token import (
    CorruptedEmailTokenError,
    EmailTokenAlreadyUsedError,
)


@dataclass(frozen=True)
class EmailVerificationInputDTO:
    token: str


@dataclass(frozen=True)
class EmailVerificationOutputDTO:
    email: Optional[str]


class EmailVerification(
    Interactor[EmailVerificationInputDTO, EmailVerificationOutputDTO]
):
    def __init__(
        self,
        repository: AuthRepository,
        uow: UoW,
        jwt_ops: JWTOperations,
        secret_key: str,
        algorithm: str,
    ):
        self.uow = uow
        self.jwt_ops = jwt_ops
        self.repository = repository
        self._secret_key = secret_key
        self._algorithm = algorithm

    async def __call__(
        self, data: EmailVerificationInputDTO
    ) -> EmailVerificationOutputDTO:
        secret_key: str = self._secret_key
        algorithm: str = self._algorithm

        payload = self.jwt_ops.decode(data.token, secret_key, algorithm)

        user_email: Optional[str] = payload.get("user_email")

        if not user_email:
            raise CorruptedEmailTokenError()

        user: Optional[DBUser] = await self.repository.get_by_email(user_email)

        if not user:
            raise UserIsNotExistsError()

        token_user_is_active: bool = payload.get("user_is_active")

        if user.is_active != token_user_is_active:
            raise EmailTokenAlreadyUsedError()

        await self.repository.set_active(user.user_id)
        await self.uow.commit()

        return EmailVerificationOutputDTO(email=user_email)
