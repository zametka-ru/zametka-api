from abc import ABC, abstractmethod

from typing import TypeVar, TypeAlias, Callable, Awaitable, AsyncContextManager

from application.common.adapters import JWT

from application.script.script_interactor import ScriptInteractor

from application.auth.sign_up import SignUp
from application.auth.sign_in import SignIn
from application.auth.refresh_token import RefreshTokenInteractor
from application.auth.email_verification import EmailVerification

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
    def sign_up(self) -> AsyncContextManager[SignUp]:
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
