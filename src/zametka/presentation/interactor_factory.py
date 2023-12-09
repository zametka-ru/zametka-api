from abc import ABC, abstractmethod

from typing import AsyncContextManager, Awaitable, Callable, TypeAlias, TypeVar

from fastapi_another_jwt_auth import AuthJWT
from starlette.background import BackgroundTasks

from zametka.application.user.email_verification import EmailVerification
from zametka.application.user.get_user import GetUser
from zametka.application.user.sign_in import SignIn
from zametka.application.user.sign_up import SignUp
from zametka.application.note.note_interactor import NoteInteractor

# G means generic
GInputDTO = TypeVar("GInputDTO")
GOutputDTO = TypeVar("GOutputDTO")

InteractorCallable: TypeAlias = Callable[[GInputDTO], Awaitable[GOutputDTO]]
InteractorPicker: TypeAlias = Callable[
    [NoteInteractor], InteractorCallable[GInputDTO, GOutputDTO]
]


class InteractorFactory(ABC):
    @abstractmethod
    def pick_note_interactor(
        self, jwt: AuthJWT, picker: InteractorPicker[GInputDTO, GOutputDTO]
    ) -> AsyncContextManager[InteractorCallable[GInputDTO, GOutputDTO]]:
        raise NotImplementedError

    @abstractmethod
    def sign_up(self, background_tasks: BackgroundTasks) -> AsyncContextManager[SignUp]:
        raise NotImplementedError

    @abstractmethod
    def sign_in(self) -> AsyncContextManager[SignIn]:
        raise NotImplementedError

    @abstractmethod
    def get_user(self, jwt: AuthJWT) -> AsyncContextManager[GetUser]:
        raise NotImplementedError

    @abstractmethod
    def email_verification(self) -> AsyncContextManager[EmailVerification]:
        raise NotImplementedError
