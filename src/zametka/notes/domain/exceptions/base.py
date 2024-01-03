from typing import Optional


class DomainError(Exception):
    def __init__(self, message: Optional[str] = None):
        self.message = message
