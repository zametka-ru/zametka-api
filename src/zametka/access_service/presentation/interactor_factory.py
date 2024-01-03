from abc import ABC, abstractmethod
from typing import AsyncContextManager

from starlette.background import BackgroundTasks

from zametka.access_service.application.common.id_provider import IdProvider
from zametka.access_service.application.verify_email import VerifyEmail
from zametka.access_service.application.get_identity import GetIdentity
from zametka.access_service.application.authorize import Authorize
from zametka.access_service.application.create_identity import CreateIdentity


class InteractorFactory(ABC):
    @abstractmethod
    def create_identity(
        self, background_tasks: BackgroundTasks
    ) -> AsyncContextManager[CreateIdentity]:
        raise NotImplementedError

    @abstractmethod
    def authorize(self) -> AsyncContextManager[Authorize]:
        raise NotImplementedError

    @abstractmethod
    def get_identity(self, id_provider: IdProvider) -> AsyncContextManager[GetIdentity]:
        raise NotImplementedError

    @abstractmethod
    def verify_email(self) -> AsyncContextManager[VerifyEmail]:
        raise NotImplementedError
