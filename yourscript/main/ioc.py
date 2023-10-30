from contextlib import asynccontextmanager
from typing import Callable, Awaitable, AsyncContextManager

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from domain.services.script_service import ScriptService

from application.script.script_interactor import ScriptInteractor
from application.script.dto import (
    CreateScriptInputDTO,
    CreateScriptOutputDTO,
    # ReadScriptInputDTO, ReadScriptOutputDTO,
    # UpdateScriptInputDTO, UpdateScriptOutputDTO,
    # DeleteScriptInputDTO, DeleteScriptOutputDTO,
)

from presentation.interactor_factory import InteractorFactory
from infrastructure.db.provider import (
    get_script_repository,
    get_auth_repository,
    get_uow,
)


class IoC(InteractorFactory):
    _session_factory: async_sessionmaker
    _script_service: ScriptService

    def __init__(self, session_factory: async_sessionmaker):
        self._session_factory = session_factory
        self._script_service = ScriptService()

    def _construct_script_interactor(self, session: AsyncSession) -> ScriptInteractor:
        script_repository = get_script_repository(session)
        auth_repository = get_auth_repository(session)
        uow = get_uow(session)
        service = self._script_service

        return ScriptInteractor(
            script_repository=script_repository,
            auth_repository=auth_repository,
            uow=uow,
            service=service,
        )

    @asynccontextmanager
    async def create_script(
        self,
    ) -> AsyncContextManager[
        Callable[[CreateScriptInputDTO], Awaitable[CreateScriptOutputDTO]]
    ]:
        async with self._session_factory() as session:
            interactor = self._construct_script_interactor(session)

            yield interactor.create
