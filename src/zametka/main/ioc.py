from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi_another_jwt_auth import AuthJWT
from fastapi_mail import FastMail
from jinja2 import Environment
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from starlette.background import BackgroundTasks

from zametka.domain.services.email_token_service import EmailTokenService
from zametka.infrastructure.adapters.auth.id_provider import TokenIdProvider

from zametka.application.user.email_verification import EmailVerification
from zametka.application.user.sign_in import SignIn
from zametka.application.user.sign_up import SignUp
from zametka.application.user.get_user import GetUser

from zametka.application.note.note_interactor import NoteInteractor
from zametka.domain.services.note_service import NoteService
from zametka.domain.services.user_service import UserService
from zametka.infrastructure.adapters.auth.mailer import MailTokenSenderImpl
from zametka.infrastructure.adapters.auth.password_hasher import PasswordHasherImpl
from zametka.infrastructure.config_loader import AuthSettings
from zametka.infrastructure.db.provider import (
    get_auth_repository,
    get_note_repository,
    get_uow,
)
from zametka.presentation.interactor_factory import (
    GInputDTO,
    GOutputDTO,
    InteractorCallable,
    InteractorFactory,
    InteractorPicker,
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

        self._note_service = NoteService()
        self._user_service = UserService()
        self._email_token_service = EmailTokenService()
        self._password_hasher = PasswordHasherImpl()

        self._auth_settings: AuthSettings = auth_settings

        self._secret_key = self._auth_settings.secret_key
        self._algorithm: str = self._auth_settings.algorithm

        self._mailer = mailer
        self._jinja_env = jinja_env

        self._token_link = token_link

    def _construct_note_interactor(
        self, session: AsyncSession, jwt: AuthJWT
    ) -> NoteInteractor:
        note_repository = get_note_repository(session)
        auth_repository = get_auth_repository(session)
        uow = get_uow(session)
        id_provider = TokenIdProvider(jwt)
        service = self._note_service

        return NoteInteractor(
            note_repository=note_repository,
            auth_repository=auth_repository,
            uow=uow,
            service=service,
            id_provider=id_provider,
        )

    @asynccontextmanager
    async def pick_note_interactor(
        self, jwt: AuthJWT, picker: InteractorPicker[GInputDTO, GOutputDTO]
    ) -> AsyncIterator[InteractorCallable[GInputDTO, GOutputDTO]]:
        async with self._session_factory() as session:
            interactor = self._construct_note_interactor(session, jwt)
            yield picker(interactor)

    @asynccontextmanager
    async def sign_up(self, background_tasks: BackgroundTasks) -> AsyncIterator[SignUp]:
        async with self._session_factory() as session:
            interactor = SignUp(
                repository=get_auth_repository(session),
                pwd_context=self._password_hasher,
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
            )

            yield interactor

    @asynccontextmanager
    async def sign_in(self) -> AsyncIterator[SignIn]:
        async with self._session_factory() as session:
            interactor = SignIn(
                repository=get_auth_repository(session),
                pwd_context=self._password_hasher,
                user_service=self._user_service,
            )

            yield interactor

    @asynccontextmanager
    async def get_user(self, jwt: AuthJWT) -> AsyncIterator[GetUser]:
        async with self._session_factory() as session:
            interactor = GetUser(
                auth_repository=get_auth_repository(session),
                id_provider=TokenIdProvider(jwt),
            )

            yield interactor

    @asynccontextmanager
    async def email_verification(self) -> AsyncIterator[EmailVerification]:
        async with self._session_factory() as session:
            interactor = EmailVerification(
                repository=get_auth_repository(session),
                uow=get_uow(session),
                secret_key=self._secret_key,
                algorithm=self._algorithm,
                email_token_service=self._email_token_service,
            )

            yield interactor
