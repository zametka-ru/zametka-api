from contextlib import asynccontextmanager
from typing import AsyncIterator

from aiohttp import ClientSession
from fastapi_mail import FastMail
from jinja2 import Environment

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from zametka.access_service.application.common.id_provider import IdProvider

from zametka.access_service.application.verify_email import VerifyEmail
from zametka.access_service.application.authorize import Authorize
from zametka.access_service.application.create_identity import CreateIdentity
from zametka.access_service.application.get_identity import GetIdentity
from zametka.access_service.infrastructure.id_provider import UserProviderImpl

from zametka.access_service.infrastructure.mail_token_sender import MailTokenSenderImpl
from zametka.access_service.infrastructure.config_loader import AuthConfig
from zametka.access_service.infrastructure.persistence.provider import (
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
        auth_settings: AuthConfig,
        mailer: FastMail,
        jinja_env: Environment,
        token_link: str,
    ):
        self._session_factory = session_factory

        self._auth_settings: AuthConfig = auth_settings

        self._mailer = mailer
        self._jinja_env = jinja_env

        self._token_link = token_link

        self._aiohttp_session = ClientSession()

    @asynccontextmanager
    async def create_identity(self) -> AsyncIterator[CreateIdentity]:
        async with self._session_factory() as session:
            interactor = CreateIdentity(
                user_repository=get_user_repository(session),
                token_sender=MailTokenSenderImpl(
                    jinja=self._jinja_env,
                    mail=self._mailer,
                    token_link=self._token_link,
                ),
                uow=get_uow(session),
            )

            yield interactor

    @asynccontextmanager
    async def authorize(self) -> AsyncIterator[Authorize]:
        async with self._session_factory() as session:
            interactor = Authorize(
                user_repository=get_user_repository(session),
            )

            yield interactor

    @asynccontextmanager
    async def get_identity(self, id_provider: IdProvider) -> AsyncIterator[GetIdentity]:
        async with self._session_factory() as session:
            interactor = GetIdentity(
                user_provider=UserProviderImpl(
                    user_repository=get_user_repository(session),
                    id_provider=id_provider,
                ),
            )

            yield interactor

    @asynccontextmanager
    async def verify_email(self) -> AsyncIterator[VerifyEmail]:
        async with self._session_factory() as session:
            interactor = VerifyEmail(
                user_repository=get_user_repository(session),
                uow=get_uow(session),
            )

            yield interactor
