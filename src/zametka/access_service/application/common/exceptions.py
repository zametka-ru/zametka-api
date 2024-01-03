from typing import Optional, Any

from zametka.access_service.domain.exceptions.base import DomainError


class ApplicationError(DomainError):
    def __init__(
        self, message: Optional[str] = None, detail: Optional[dict[str, Any]] = None
    ):
        super().__init__(message)

        self.detail = detail or {"detail": self.message}


class EventIsNotDeliveredError(ApplicationError):
    pass
