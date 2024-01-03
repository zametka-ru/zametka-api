import logging

from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from zametka.access_service.application.common.event import EventEmitter
from zametka.access_service.application.common.exceptions import (
    EventIsNotDeliveredError,
)
from zametka.access_service.application.common.token_sender import MailTokenSender
from zametka.access_service.application.common.interactor import Interactor
from zametka.access_service.application.common.repository import UserIdentityRepository
from zametka.access_service.application.common.uow import UoW
from zametka.access_service.application.dto import UserIdentityDTO, UserCreatedEvent
from zametka.access_service.domain.services.email_token_service import EmailTokenService
from zametka.access_service.domain.services.user_identity_service import (
    UserIdentityService,
)
from zametka.access_service.domain.value_objects.email_token import EmailToken
from zametka.access_service.domain.value_objects.user_email import UserEmail
from zametka.access_service.domain.value_objects.user_identity_id import UserIdentityId
from zametka.access_service.domain.value_objects.user_raw_password import (
    UserRawPassword,
)

EMAIL_SUBJECT = "Завершите регистрацию в приложении zametka."


@dataclass(frozen=True)
class IdentityInputDTO:
    email: str
    password: str
    additional_info: dict[str, Any]


class CreateIdentity(Interactor[IdentityInputDTO, UserIdentityDTO]):
    def __init__(
        self,
        user_repository: UserIdentityRepository,
        token_sender: MailTokenSender,
        uow: UoW,
        service: UserIdentityService,
        email_token_service: EmailTokenService,
        emitter: EventEmitter[UserCreatedEvent],
        secret_key: str,
        algorithm: str,
    ):
        self.uow = uow
        self.service = service
        self.token_sender = token_sender
        self.user_repository = user_repository
        self.email_token_service = email_token_service
        self.emitter = emitter
        self._secret_key = secret_key
        self._algorithm = algorithm

    async def __call__(self, data: IdentityInputDTO) -> UserIdentityDTO:
        email = UserEmail(data.email)
        raw_password = UserRawPassword(data.password)
        user_identity_id = UserIdentityId(value=uuid4())

        user = self.service.create(
            email=email, raw_password=raw_password, user_identity_id=user_identity_id
        )
        user_dto = await self.user_repository.create(user)

        await self.uow.flush()

        event = UserCreatedEvent(
            identity_id=user_dto.identity_id,
            additional_info=data.additional_info,
        )

        try:
            await self.emitter.emit(event)
        except EventIsNotDeliveredError:
            await self.uow.rollback()

            logging.warning("User creation failed! Identity is rollbacked.")
            raise

        await self.uow.commit()

        secret_key: str = self._secret_key
        algorithm: str = self._algorithm

        token: EmailToken = self.email_token_service.encode_token(
            user, secret_key, algorithm
        )
        self.token_sender.send(token, subject=EMAIL_SUBJECT, to_email=user.email)

        return user_dto
