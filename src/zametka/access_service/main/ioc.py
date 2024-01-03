from contextlib import asynccontextmanager
from typing import AsyncIterator

from aiohttp import ClientSession
from fastapi_mail import FastMail
from jinja2 import Environment

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from starlette.background import BackgroundTasks

from zametka.access_service.application.common.event import EventHandler
from zametka.access_service.application.common.id_provider import IdProvider
from zametka.access_service.application.dto import UserCreatedEvent
from zametka.access_service.domain.services.email_token_service import EmailTokenService

from zametka.access_service.application.verify_email import VerifyEmail
from zametka.access_service.application.authorize import Authorize
from zametka.access_service.application.create_identity import CreateIdentity
from zametka.access_service.application.get_identity import GetIdentity

from zametka.access_service.domain.services.user_identity_service import (
    UserIdentityService,
)
from zametka.access_service.infrastructure.event_handler import UserCreatedEventHandler
from zametka.access_service.infrastructure.event_sender import EventSenderImpl
from zametka.access_service.infrastructure.event_emitter import EventEmitterImpl
from zametka.access_service.infrastructure.mailer import MailTokenSenderImpl
from zametka.access_service.infrastructure.config_loader import AuthSettings
from zametka.access_service.infrastructure.db.provider import (
    get_user_repository,
    get_uow,
)
from zametka.access_service.presentation.interactor_factory import (
    InteractorFactory,
)


class IoC(InteractorFactory):
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        auth_settings: AuthSettings,
        mailer: FastMail,
        jinja_env: Environment,
        token_link: str,
    ):
        self._session_factory = session_factory

        self._user_service = UserIdentityService()
        self._email_token_service = EmailTokenService()

        self._auth_settings: AuthSettings = auth_settings

        self._secret_key = self._auth_settings.secret_key
        self._algorithm: str = self._auth_settings.algorithm

        self._mailer = mailer
        self._jinja_env = jinja_env

        self._token_link = token_link

        self._aiohttp_session = ClientSession()

    @asynccontextmanager
    async def create_identity(
        self, background_tasks: BackgroundTasks
    ) -> AsyncIterator[CreateIdentity]:
        event_sender: EventSenderImpl = EventSenderImpl(self._aiohttp_session)
        user_created_event_handler: EventHandler[
            UserCreatedEvent
        ] = UserCreatedEventHandler(event_sender)
        event_emitter: EventEmitterImpl[UserCreatedEvent] = EventEmitterImpl()

        event_emitter.on(UserCreatedEvent, user_created_event_handler)

        async with self._session_factory() as session:
            interactor = CreateIdentity(
                user_repository=get_user_repository(session),
                token_sender=MailTokenSenderImpl(
                    jinja=self._jinja_env,
                    mail=self._mailer,
                    background_tasks=background_tasks,
                    token_link=self._token_link,
                ),
                secret_key=self._secret_key,
                algorithm=self._algorithm,
                service=self._user_service,
                uow=get_uow(session),
                email_token_service=self._email_token_service,
                emitter=event_emitter,
            )

            yield interactor

    @asynccontextmanager
    async def authorize(self) -> AsyncIterator[Authorize]:
        async with self._session_factory() as session:
            interactor = Authorize(
                user_repository=get_user_repository(session),
                user_service=self._user_service,
            )

            yield interactor

    @asynccontextmanager
    async def get_identity(self, id_provider: IdProvider) -> AsyncIterator[GetIdentity]:
        async with self._session_factory() as session:
            interactor = GetIdentity(
                user_repository=get_user_repository(session),
                id_provider=id_provider,
                user_service=self._user_service,
            )

            yield interactor

    @asynccontextmanager
    async def verify_email(self) -> AsyncIterator[VerifyEmail]:
        async with self._session_factory() as session:
            interactor = VerifyEmail(
                user_repository=get_user_repository(session),
                uow=get_uow(session),
                secret_key=self._secret_key,
                algorithm=self._algorithm,
                email_token_service=self._email_token_service,
            )

            yield interactor
