from typing import Generic, TypeVar, Protocol

InputDTO = TypeVar("InputDTO")
OutputDTO = TypeVar("OutputDTO")


class Interactor(Generic[InputDTO, OutputDTO]):
    def __call__(self, data: InputDTO) -> OutputDTO:
        raise NotImplementedError


class CRUDInteractor(Protocol):
    async def create(self, data: InputDTO) -> OutputDTO:
        raise NotImplementedError

    async def read(self, data: InputDTO) -> OutputDTO:
        raise NotImplementedError

    async def update(self, data: InputDTO) -> OutputDTO:
        raise NotImplementedError

    async def delete(self, data: InputDTO) -> OutputDTO:
        raise NotImplementedError


InteractorT = TypeVar("InteractorT")
CRUDInteractorT = TypeVar("CRUDInteractorT")
