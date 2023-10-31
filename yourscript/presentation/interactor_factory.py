from abc import abstractmethod, ABC

from typing import AsyncContextManager, Callable, Awaitable

from application.common.adapters import JWT
from application.script.dto import (
    ReadScriptInputDTO,
    ReadScriptOutputDTO,
    UpdateScriptInputDTO,
    UpdateScriptOutputDTO,
    DeleteScriptInputDTO,
    DeleteScriptOutputDTO,
    CreateScriptOutputDTO,
    CreateScriptInputDTO,
)


class InteractorFactory(ABC):
    @abstractmethod
    def create_script(
        self, jwt: JWT
    ) -> AsyncContextManager[
        Callable[[CreateScriptInputDTO], Awaitable[CreateScriptOutputDTO]]
    ]:
        raise NotImplementedError

    @abstractmethod
    def read_script(
        self, jwt: JWT
    ) -> AsyncContextManager[
        Callable[[ReadScriptInputDTO], Awaitable[ReadScriptOutputDTO]]
    ]:
        raise NotImplementedError

    @abstractmethod
    def update_script(
        self, jwt: JWT
    ) -> AsyncContextManager[
        Callable[[UpdateScriptInputDTO], Awaitable[UpdateScriptOutputDTO]]
    ]:
        raise NotImplementedError

    @abstractmethod
    def delete_script(
        self, jwt: JWT
    ) -> AsyncContextManager[
        Callable[[DeleteScriptInputDTO], Awaitable[DeleteScriptOutputDTO]]
    ]:
        raise NotImplementedError
