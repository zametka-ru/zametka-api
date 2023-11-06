from abc import ABC, abstractmethod

from typing import TypeVar, TypeAlias, Callable, Awaitable, AsyncContextManager

from starlette.background import BackgroundTasks

from yourscript.application.common.adapters import JWT
from yourscript.application.script.script_interactor import ScriptInteractor

from yourscript.application.auth.sign_up import SignUp
from yourscript.application.auth.sign_in import SignIn
from yourscript.application.auth.refresh_token import RefreshTokenInteractor
from yourscript.application.auth.email_verification import EmailVerification

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
    def sign_in(self, jwt: JWT) -> AsyncContextManager[SignIn]:
        raise NotImplementedError

    @abstractmethod
    def refresh_token(self, jwt: JWT) -> AsyncContextManager[RefreshTokenInteractor]:
        raise NotImplementedError

    @abstractmethod
    def email_verification(self) -> AsyncContextManager[EmailVerification]:
        raise NotImplementedError