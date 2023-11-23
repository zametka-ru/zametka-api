from abc import ABC, abstractmethod
from typing import AsyncContextManager, Awaitable, Callable, TypeAlias, TypeVar

from starlette.background import BackgroundTasks

from yourscript.application.auth.email_verification import EmailVerification
from yourscript.application.auth.get_user import GetUser
from yourscript.application.auth.sign_in import SignIn
from yourscript.application.auth.sign_up import SignUp
from yourscript.application.common.adapters import JWT
from yourscript.application.script.script_interactor import ScriptInteractor

# G means generic
GInputDTO = TypeVar("GInputDTO")
GOutputDTO = TypeVar("GOutputDTO")

InteractorCallable: TypeAlias = Callable[[GInputDTO], Awaitable[GOutputDTO]]
InteractorPicker: TypeAlias = Callable[
    [ScriptInteractor], InteractorCallable[GInputDTO, GOutputDTO]
]


class InteractorFactory(ABC):
    @abstractmethod
    def pick_script_interactor(
        self, jwt: JWT, picker: InteractorPicker[GInputDTO, GOutputDTO]
    ) -> AsyncContextManager[InteractorCallable[GInputDTO, GOutputDTO]]:
        raise NotImplementedError

    @abstractmethod
    def sign_up(self, background_tasks: BackgroundTasks) -> AsyncContextManager[SignUp]:
        raise NotImplementedError

    @abstractmethod
    def sign_in(self) -> AsyncContextManager[SignIn]:
        raise NotImplementedError

    @abstractmethod
    def get_user(self, jwt: JWT) -> AsyncContextManager[GetUser]:
        raise NotImplementedError

    @abstractmethod
    def email_verification(self) -> AsyncContextManager[EmailVerification]:
        raise NotImplementedError
