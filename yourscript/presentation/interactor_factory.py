from abc import abstractmethod, ABC

from typing import AsyncContextManager

from application.script.script_interactor import ScriptInteractor


class InteractorFactory(ABC):
    @abstractmethod
    async def create_script(self) -> AsyncContextManager[ScriptInteractor]:
        raise NotImplementedError

    @abstractmethod
    async def read_script(self) -> AsyncContextManager[ScriptInteractor]:
        raise NotImplementedError

    @abstractmethod
    async def update_script(self) -> AsyncContextManager[ScriptInteractor]:
        raise NotImplementedError

    @abstractmethod
    async def delete_script(self) -> AsyncContextManager[ScriptInteractor]:
        raise NotImplementedError
