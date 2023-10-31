from abc import ABC
from contextlib import asynccontextmanager
from typing import TypeVar, TypeAlias, Callable, Awaitable, AsyncIterator

from application.common.adapters import JWT
from application.script.script_interactor import ScriptInteractor

# G means generic
GInputDTO = TypeVar("GInputDTO")
GOutputDTO = TypeVar("GOutputDTO")

InteractorCallable: TypeAlias = Callable[[GInputDTO], Awaitable[GOutputDTO]]
InteractorPicker: TypeAlias = Callable[
    [ScriptInteractor], InteractorCallable[GInputDTO, GOutputDTO]
]


class InteractorFactory(ABC):
    @asynccontextmanager
    def pick_script_interactor(
        self, jwt: JWT, picker: InteractorPicker[GInputDTO, GOutputDTO]
    ) -> AsyncIterator[InteractorCallable[GInputDTO, GOutputDTO]]:
        raise NotImplementedError
