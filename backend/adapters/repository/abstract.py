from abc import ABC

from sqlalchemy.orm import Session


class AbstractRepository(ABC):
    """Abstract implementation of repository"""

    session: Session

    def __init__(self, session: Session) -> None:
        self.session = session
